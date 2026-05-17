import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS knowledge_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            keywords TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS prompts (
            name TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            description TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            project TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            intent TEXT,
            confidence REAL,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emoji TEXT DEFAULT '📦',
            price REAL NOT NULL,
            original_price REAL DEFAULT 0,
            tags TEXT DEFAULT '',
            match_score REAL DEFAULT 0.8,
            reason TEXT DEFAULT '',
            category TEXT DEFAULT '综合',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS intent_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            intent_name TEXT NOT NULL,
            sub_intent TEXT DEFAULT '',
            keywords TEXT NOT NULL,
            entities TEXT DEFAULT '',
            priority INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS user_profiles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            rfm_segment TEXT DEFAULT '',
            preferences TEXT DEFAULT '',
            budget TEXT DEFAULT '',
            level TEXT DEFAULT ''
        );
    ''')
    _seed_defaults(conn)
    conn.commit()
    conn.close()

def _seed_defaults(conn):
    c = conn.execute("SELECT COUNT(*) FROM categories")
    if c.fetchone()[0] > 0:
        return

    cats = [
        (1, '退款相关', '退款流程、条件、到账时间等'),
        (2, '约课相关', '课程预约、取消、排队规则'),
        (3, '会员卡', '卡种对比、价格、权益说明'),
        (4, '门店信息', '地址、营业时间、设施查询'),
        (5, '账户问题', '登录、冻结、信息修改'),
        (6, '健身指导', '器材使用、训练计划、饮食建议'),
        (7, '商品推荐', '蛋白粉、器材、服饰推荐'),
    ]
    conn.executemany("INSERT OR IGNORE INTO categories(id,name,description) VALUES(?,?,?)", cats)

    entries = [
        (1, '怎么申请退款？', '您可在APP「我的-订单」中找到对应订单，点击「申请退款」。月卡未使用可全额退，已使用按天数折算。退款1-3个工作日原路返回。', '退款,申请,退费'),
        (1, '退款多久到账？', '审核通过后1-3个工作日到账，原路返回至您的支付账户。超3个工作日未到账请联系客服。', '退款,到账,时间'),
        (2, '怎么预约团课？', '打开APP→「课程」→选择门店和课程→点击「立即预约」。热门课程需提前2天预约，每人每周最多预约3节团课。', '约课,团课,预约,课程'),
        (2, '如何取消课程预约？', '开课前2小时可在APP「我的-我的课程」中取消。超时取消会计入爽约次数，30天内爽约3次将限制预约7天。', '取消,预约,课程,爽约'),
        (3, '年卡和月卡有什么区别？', '月卡199元/月，灵活按月付费；季卡499元/季（省98元）；年卡1,699元/年（省689元，折合141元/月）。所有卡种通用全国门店，年卡额外赠送2次私教体验课。', '年卡,月卡,价格,对比,会员卡'),
        (3, '会员卡可以暂停吗？', '年卡用户每年可申请一次免费停卡（7-30天），月卡不支持停卡。请提前3天在APP「我的-会员卡-停卡申请」中操作。', '停卡,暂停,会员卡'),
        (4, '门店营业时间是几点？', '大部分门店营业时间为6:00-23:00，部分商场店为10:00-22:00。具体请查看APP门店详情页。', '营业时间,门店,开门,关门'),
        (4, '怎么找到最近的门店？', '打开APP首页→「门店」→系统自动定位推荐最近门店。支持按设施（淋浴/停车/团课室）筛选。全国2000+门店覆盖40+城市。', '门店,最近,地址,位置'),
        (5, '账号被冻结了怎么办？', '账号冻结通常是因支付异常或违规操作。请拨打客服电话或联系在线客服，提供注册手机号，我们会在1个工作日内核实处理。', '冻结,账号,解封'),
        (6, '新手健身有什么推荐课程？', '建议从入门团课开始：瑜伽（提升柔韧性）、BodyPump（基础力量）、Zumba（趣味有氧）。搭配「新手7天体验计划」循序渐进。', '新手,入门,课程推荐,健身'),
        (6, '想增肌应该怎么练？', '建议每周3-4次力量训练，胸背腿循环。搭配高蛋白饮食（1.6-2g/kg体重）。推荐使用自由重量（杠铃哑铃）和复合动作（深蹲/卧推/硬拉）。需要蛋白粉推荐可以告诉我。', '增肌,力量,训练,蛋白粉'),
        (7, '推荐一款适合新手的蛋白粉', '推荐「乳清蛋白粉-基础款」299元/2.2kg，蛋白质含量75%，易吸收，适合新手。口感好、性价比高，搭配训练后30分钟内饮用效果最佳。', '蛋白粉,新手,乳清蛋白,补剂'),
        (7, '想减肥买什么装备？', '推荐组合：① 智能跳绳 89元（高效燃脂）② 瑜伽垫 59元（家庭训练必备）③ 运动手环 199元（心率监测）。先坚持21天再考虑加购器械，避免闲置。', '减肥,减脂,装备,跳绳,瑜伽垫'),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO knowledge_entries(category_id,question,answer,keywords) VALUES(?,?,?,?)",
        entries
    )

    prompt_seeds = [
        ('customer_service_system', '''你是乐刻运动的AI智能客服"小乐"，你的职责是帮助用户解答问题。

## 角色设定
- 你是乐刻运动的官方客服，服务全国2000+门店、1000万+注册用户
- 语气友好、专业、简洁，用词口语化但不失专业感
- 回答控制在200字以内，复杂问题分点说明

## 知识范围
- 会员卡（月卡/季卡/年卡）的购买、使用、退款政策
- 课程预约、取消规则
- 门店地址、营业时间、设施查询
- 账户相关问题（登录、冻结、信息修改）
- 退款流程和时效

## 行为约束
- 严格基于知识库内容回答，不要编造信息
- 不确定的问题请说"我需要帮您核实一下，建议联系人工客服"
- 涉及退款金额、账户安全等敏感问题，引导用户联系人工客服
- 不要承诺知识库之外的优惠政策

## 回答格式
- 先给出直接答案
- 必要时补充操作步骤（1. 2. 3.）
- 结尾可附相关链接提示（如"详情可在APP「我的-帮助中心」查看"）''', '客服系统Prompt'),

        ('customer_service_fewshot', '''示例1:
用户: 我要退款
客服: 您好，退款可前往APP「我的-订单」中找到对应订单申请。请问您要退的是会员卡还是课程呢？月卡未使用可全额退，已使用部分按天数折算哦。

示例2:
用户: 预约的课怎么取消
客服: 开课前2小时可在APP「我的-我的课程」中取消预约。注意超时取消会计入爽约次数，30天内爽约3次将暂停预约权限7天。

示例3:
用户: 最近的店在哪
客服: 打开APP首页点击「门店」，系统会自动定位并推荐离您最近的门店。您也可以按设施（淋浴/停车）筛选，全国2000+门店任您选择~''', '客服Few-shot示例'),

        ('shopping_guide_system', '''你是乐刻运动的AI导购助手"小乐"，你的职责是帮助用户找到最适合的健身产品和课程。

## 角色设定
- 你是专业的健身顾问和导购，了解健身器材、运动服饰、营养补剂
- 语气亲切、有活力，像一个懂健身的朋友
- 推荐时说明理由，让用户理解为什么适合

## 推荐策略
- 先了解用户的基本情况：健身目标、当前水平、预算范围
- 基于用户画像和历史行为做个性化推荐
- 推荐3个左右选项，说明各自的匹配理由
- 优先推荐高匹配度（>80%）的商品

## 行为约束
- 严格基于知识库中的商品信息推荐
- 不确定产品细节时诚实说明
- 不要夸大产品功效，特别是营养补剂类
- 提醒用户根据自身情况选择，必要时咨询教练

## 回复格式
- 先共情理解用户需求（一句话）
- 推荐3个产品/课程，附带简短理由
- 结尾可追问是否需要更详细的对比''', '导购系统Prompt'),

        ('shopping_guide_fewshot', '''示例1:
用户: 我是新手想减肥，预算500以内
客服: 刚入门的话，我们推荐从这几样开始：
① 智能跳绳 89元 - 燃脂效率最高，每天15分钟就能见效
② 瑜伽垫 59元 - 在家就能练，跟APP课程一起效果翻倍
③ 运动手环 199元 - 监控心率和卡路里，让每次运动都有数据可看
总共不到350元，剩下的预算可以先留着，坚持21天后再考虑加购~

示例2:
用户: 想买蛋白粉，不要太多添加剂的
客服: 推荐「乳清蛋白粉-纯净版」349元/2kg，配料表只有乳清蛋白+大豆卵磷脂，无香精色素。蛋白质含量80%，适合对成分有要求的朋友。搭配训练后30分钟内喝，吸收效果最佳。''', '导购Few-shot示例'),
    ]
    conn.executemany("INSERT OR IGNORE INTO prompts(name,content,description) VALUES(?,?,?)", prompt_seeds)

    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('deepseek_api_key','')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('deepseek_model','deepseek-chat')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('confidence_threshold','0.75')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('rec_weight_rfm','40')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('rec_weight_cf','25')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('rec_weight_llm','35')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('temperature','0.7')")
    conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('max_tokens','2048')")

    # Intent rules
    intent_seeds = [
        ('customer_service', '退款咨询', '售后', '退款,退费,退钱,退货,退卡', '订单,退款金额', 10),
        ('customer_service', '约课咨询', '课程预约', '约课,预约,课程,团课,订课,取消预约', '课程类型,时间', 10),
        ('customer_service', '会员卡咨询', '卡种对比', '年卡,月卡,季卡,会员卡,价格,多少钱,区别,对比,停卡', '卡种,价格', 10),
        ('customer_service', '门店查询', '位置信息', '门店,地址,在哪,营业时间,开门,关门,最近,怎么去', '地理位置', 10),
        ('customer_service', '账户问题', '账号异常', '冻结,封号,登录,密码,账号,账户,解封', '账号状态', 10),
        ('customer_service', '健身指导', '产品推荐', '蛋白粉,补剂,推荐,装备,器材,减肥,增肌,新手,入门,课程推荐', '训练目标,产品类型', 5),
        ('shopping_guide', '减脂推荐', '', '减肥,减脂,瘦,减重,燃脂,有氧', '卡路里,时长', 10),
        ('shopping_guide', '增肌推荐', '', '增肌,力量,蛋白,肌肉,壮,增重,维度', '蛋白质,组数', 10),
        ('shopping_guide', '瑜伽推荐', '', '瑜伽,柔韧,拉伸,放松,冥想', '课程类型', 10),
        ('shopping_guide', '装备推荐', '', '装备,器材,跳绳,哑铃,瑜伽垫,手环,器械', '预算,使用场景', 10),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO intent_rules(project,intent_name,sub_intent,keywords,entities,priority) VALUES(?,?,?,?,?,?)",
        intent_seeds
    )

    # Products catalog
    product_seeds = [
        ('乳清蛋白粉-基础款', '🥛', 299, 399, '高蛋白,易吸收,新手友好', 0.92, '75%蛋白质含量，训练后快速补充', '营养补剂'),
        ('智能跳绳-燃脂版', '⭕', 89, 129, '便携,计数,高效燃脂', 0.88, '每天15分钟高效燃脂，APP记录数据', '有氧器材'),
        ('专业瑜伽垫-加厚款', '🧘', 59, 79, '防滑,加厚,环保', 0.85, '6mm厚度保护关节，适合初学者', '瑜伽装备'),
        ('运动手环Pro', '⌚', 199, 259, '心率监测,运动追踪,防水', 0.82, '实时监控运动数据，科学指导训练', '智能设备'),
        ('增肌蛋白粉-进阶版', '💪', 449, 549, '高纯度,增肌配方,BCAA', 0.78, '80%蛋白质+5g BCAA，适合增肌期', '营养补剂'),
        ('BodyPump杠铃课程', '🏋️', 199, 299, '力量训练,全身塑形,团课', 0.76, '60分钟全身力量训练，适合塑形', '课程'),
        ('乳清蛋白粉-纯净版', '🥛', 349, 429, '无添加,纯净配方', 0.80, '配料表只有乳清蛋白+大豆卵磷脂', '营养补剂'),
        ('弹力带套装', '🎗️', 39, 59, '便携,多阻力,家用', 0.74, '5条不同阻力，家庭/出差训练必备', '小型器材'),
        ('运动速干T恤', '👕', 99, 149, '速干,透气,轻量', 0.70, '透气速干面料，多色可选', '运动服饰'),
        ('筋膜枪Mini', '🔫', 259, 359, '按摩,恢复,便携', 0.72, '运动后深层放松，缓解肌肉酸痛', '恢复设备'),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO products(name,emoji,price,original_price,tags,match_score,reason,category) VALUES(?,?,?,?,?,?,?,?)",
        product_seeds
    )

    # User profiles
    profile_seeds = [
        ('p1', '张三', '高价值·活跃用户', '增肌,力量训练,高蛋白', '中高', '中级'),
        ('p2', '李四', '新用户·潜力', '减脂,瑜伽,低卡', '低', '新手'),
        ('p3', '王五', '流失预警', 'CrossFit,功能性训练', '高', '高级'),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO user_profiles(id,name,rfm_segment,preferences,budget,level) VALUES(?,?,?,?,?,?)",
        profile_seeds
    )

if __name__ == '__main__':
    init_db()
    print(f'Database initialized at {DB_PATH}')
