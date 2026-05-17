const DEEPSEEK_KEY = 'sk-d1df0d8f07fe49f9b5fe5e425ff57d86';
const DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions';
const MODEL = 'deepseek-v4-pro';

const PRODUCTS = [{id:"prod_001","name":"新人7天体验卡","category":"会员卡","subcategory":"体验卡","price":9.9,"original_price":99,"target":["新手","价格敏感","观望用户"],"tags":["短期","体验","高性价比","新用户专享"],"description":"7天无限次健身，涵盖所有门店和基础操课，适合首次体验乐刻的新用户。每人限购1次，到期后可续购正式会员卡。","popularity":98},{id:"prod_002","name":"月卡会员","category":"会员卡","subcategory":"月卡","price":299,"original_price":299,"target":["灵活健身","短期需求","学生"],"tags":["按月付费","灵活","无合约"],"description":"按月付费，无需长期绑定。全城门店通用，不限次数。支持自动续费（享9折优惠），随时可取消。最灵活的会员方案。","popularity":90},{id:"prod_003","name":"季卡会员","category":"会员卡","subcategory":"季卡","price":799,"original_price":897,"target":["季度计划","规律健身"],"tags":["季度","省¥98","稳定"],"description":"三个月会员，比月卡×3省¥98。适合有明确季度健身计划的用户。全城通用、不限次数、含1次体测。","popularity":75},{id:"prod_004","name":"年卡会员","category":"会员卡","subcategory":"年卡","price":2399,"original_price":3588,"target":["长期健身","深度用户","高性价比"],"tags":["年卡","省¥1189","性价比之王","含体测"],"description":"年度会员最具性价比，比月卡×12省¥1189。全城通用、无限次、含4次免费体测、每月2次携友名额、生日月额外7天。","popularity":82},{id:"prod_005","name":"学生年卡","category":"会员卡","subcategory":"年卡","price":1919,"original_price":2399,"target":["学生","年轻用户","预算有限"],"tags":["学生专享","8折","需认证"],"description":"全日制在校大学生专属年卡，完成学生认证后享8折优惠。享受年卡全部权益。每年需重新认证。","popularity":65},{id:"prod_007","name":"零基础瑜伽入门（8节）","category":"私教课","subcategory":"瑜伽","price":1599,"original_price":2392,"target":["新手","女性","柔韧性训练","减压"],"tags":["私教","瑜伽","零基础","小班"],"description":"1对1私教瑜伽入门课包，8节课系统学习基础体式。含体态评估、呼吸法、核心力量建立。适合从未接触过瑜伽的初学者。","popularity":72},{id:"prod_008","name":"力量训练入门课包（10节）","category":"私教课","subcategory":"力量训练","price":2490,"original_price":2990,"target":["新手","男性","增肌","塑形"],"tags":["私教","力量","入门","增肌"],"description":"系统学习力量训练基础：深蹲/硬拉/卧推/划船/推举五大动作。含体态评估、训练计划定制、营养建议。10节课包教包会。","popularity":68},{id:"prod_010","name":"产后恢复私教课（10节）","category":"私教课","subcategory":"康复","price":2990,"original_price":3490,"target":["产后妈妈","女性","恢复"],"tags":["私教","产后","康复","腹直肌"],"description":"专为产后妈妈设计，含盆底肌修复、腹直肌分离恢复、核心重建、体态调整。教练具备产后康复认证。10节课为1个恢复周期。","popularity":45},{id:"prod_011","name":"拉伸放松课（单次）","category":"私教课","subcategory":"拉伸","price":99,"original_price":199,"target":["久坐族","运动后","办公人群"],"tags":["拉伸","放松","单次","便宜"],"description":"30分钟专业被动拉伸，缓解肌肉紧张、改善体态。适合久坐办公人群、运动后放松。也适合想先体验私教服务的用户。","popularity":80},{id:"prod_012","name":"HIIT高效燃脂团课","category":"团课","subcategory":"HIIT","price":0,"original_price":0,"target":["燃脂","减肥","体能","年轻"],"tags":["团课","免费","高强度","燃脂"],"description":"高强度间歇训练，30分钟消耗500+卡路里。包含burpee、波比跳、登山跑等动作。难度L2-L3，建议有一定基础。会员免费。","popularity":92},{id:"prod_013","name":"流瑜伽团课","category":"团课","subcategory":"瑜伽","price":0,"original_price":0,"target":["女性","柔韧","减压","放松"],"tags":["团课","免费","瑜伽","柔韧"],"description":"动态流瑜伽，呼吸与动作同步。提升身体柔韧性和平衡力。难度L1-L2，新手友好。每次60分钟，会员免费。","popularity":88},{id:"prod_014","name":"动感单车团课","category":"团课","subcategory":"单车","price":0,"original_price":0,"target":["燃脂","音乐","年轻","团课爱好者"],"tags":["团课","免费","单车","燃脂","音乐"],"description":"沉浸式动感单车体验，配合灯光音乐节奏骑行。45分钟消耗400-600卡。难度L2，氛围感强。最受欢迎团课之一。","popularity":95},{id:"prod_016","name":"Zumba尊巴热舞","category":"团课","subcategory":"舞蹈","price":0,"original_price":0,"target":["女性","舞蹈","趣味","社交"],"tags":["团课","免费","舞蹈","趣味","社交"],"description":"拉丁风格健身舞蹈课程，跟随动感音乐自由舞动。无基础要求，开心第一。每次60分钟，消耗400-500卡。会员免费。","popularity":78},{id:"prod_018","name":"普拉提团课","category":"团课","subcategory":"普拉提","price":0,"original_price":0,"target":["女性","体态","核心","康复"],"tags":["团课","免费","普拉提","体态","优雅"],"description":"垫上普拉提，强调核心控制与精确动作。改善体态、缓解腰痛。难度L1，新手友好。每次50分钟，会员免费。","popularity":76},{id:"prod_019","name":"乳清蛋白粉（巧克力味）","category":"营养补剂","subcategory":"蛋白粉","price":299,"original_price":399,"target":["增肌","健身爱好者","男性"],"tags":["蛋白粉","增肌","营养","巧克力"],"description":"进口乳清蛋白，每份25g蛋白质，5.5g BCAA。巧克力口味，口感细腻。运动后30分钟内饮用最佳。2磅装约30次份。","popularity":62},{id:"prod_024","name":"专业健身手套","category":"运动装备","subcategory":"手套","price":79,"original_price":129,"target":["力量训练","防滑","护手"],"tags":["手套","防滑","护手","耐磨"],"description":"透气网面+加厚掌心垫，防滑耐磨，保护手掌不起茧。腕部魔术贴可调节松紧。S/M/L三码可选。","popularity":60},{id:"prod_025","name":"瑜伽垫（6mm加厚）","category":"运动装备","subcategory":"瑜伽垫","price":129,"original_price":199,"target":["瑜伽","普拉提","居家健身"],"tags":["瑜伽垫","防滑","加厚","环保"],"description":"TPE环保材质，6mm加厚缓冲，双面防滑纹理。含背带便于携带。尺寸183×61cm。可水洗清洁。","popularity":72},{id:"prod_026","name":"弹力带套装（5条装）","category":"运动装备","subcategory":"弹力带","price":49,"original_price":79,"target":["居家健身","热身","康复","新手"],"tags":["弹力带","便携","多阻力","入门"],"description":"5条不同阻力弹力带（10-50磅），满足不同部位训练需求。含收纳袋及训练指导手册。居家/出差健身必备。","popularity":68},{id:"prod_030","name":"线上减脂训练营（21天）","category":"线上课","subcategory":"减脂","price":199,"original_price":399,"target":["减脂","居家","自律"],"tags":["线上","减脂","21天","社群","打卡"],"description":"21天线上减脂计划：每日视频课程（30-40min）+ 饮食指导 + 社群打卡监督。教练每日点评。适合无法到店的用户。","popularity":44},{id:"prod_033","name":"体态评估+训练方案（单次）","category":"私教课","subcategory":"评估","price":59,"original_price":199,"target":["新手","体态问题","久坐"],"tags":["体测","评估","定制","入门"],"description":"30分钟专业体态评估：静态/动态体态分析、柔韧性测试、核心力量评估。输出个性化训练建议。建议每季度1次。","popularity":75},{id:"prod_035","name":"筋膜枪mini版","category":"运动装备","subcategory":"电子产品","price":299,"original_price":499,"target":["运动恢复","肌肉酸痛","办公人群"],"tags":["筋膜枪","按摩","放松","便携"],"description":"迷你筋膜枪，仅重0.5kg，4档可调（1800-3200转/分）。6种按摩头适配不同部位。Type-C充电，续航6小时。","popularity":63},{id:"prod_040","name":"年卡+12节私教组合套餐","category":"会员卡","subcategory":"组合套餐","price":4599,"original_price":5987,"target":["认真健身","入门","系统训练"],"tags":["组合","年卡","私教","省¥1388"],"description":"年卡会员+12节私教课（任选类型）组合套餐。比单独购买省¥1388。适合想系统开始健身的新用户。赠体态评估1次。","popularity":55}];

const USER_PROFILES = [{id:"user_001","name":"健身新手小王","rfm_segment":"新客-低消费","rfm":{"recency":"近7天","frequency":"0次购买","monetary":"¥0"},"behavior_tags":["新手","浏览多购买少","价格敏感","对比型"],"browse_history":["prod_001","prod_007","prod_011","prod_025","prod_033"],"purchase_history":[],"preferences":{"categories":["体验卡","入门私教","基础装备"],"budget":"低预算（<¥500）","goal":"减脂+入门","level":"零基础"}},{id:"user_002","name":"资深健身者老李","rfm_segment":"老客-高消费","rfm":{"recency":"近1天","frequency":"12次购买","monetary":"¥12,800"},"behavior_tags":["忠实用户","高消费","增肌","规律","力量训练"],"browse_history":["prod_019","prod_024","prod_035"],"purchase_history":["prod_004","prod_008","prod_019","prod_024","prod_035"],"preferences":{"categories":["私教课","运动装备","营养补剂"],"budget":"高预算（无上限）","goal":"增肌+力量提升","level":"高级"}},{id:"user_003","name":"瑜伽爱好者小美","rfm_segment":"老客-中消费","rfm":{"recency":"近3天","frequency":"5次购买","monetary":"¥3,200"},"behavior_tags":["女性","瑜伽","团课活跃","社交","品质"],"browse_history":["prod_007","prod_013","prod_018","prod_025"],"purchase_history":["prod_003","prod_025"],"preferences":{"categories":["瑜伽","普拉提","运动装备"],"budget":"中预算（¥500-3000）","goal":"柔韧性+减压+体态","level":"中级"}},{id:"user_004","name":"产后恢复妈妈张姐","rfm_segment":"新客-中消费","rfm":{"recency":"近14天","frequency":"1次购买","monetary":"¥299"},"behavior_tags":["产后","女性","康复","特殊需求"],"browse_history":["prod_010","prod_018","prod_025","prod_033"],"purchase_history":["prod_002"],"preferences":{"categories":["产后恢复","普拉提","瑜伽"],"budget":"中预算（¥500-3000）","goal":"产后恢复+减重+盆底修复","level":"零基础（特殊需求）"}},{id:"user_005","name":"大学生小陈","rfm_segment":"新客-低消费","rfm":{"recency":"近30天","frequency":"0次购买","monetary":"¥0"},"behavior_tags":["学生","预算有限","年轻","团课","社交"],"browse_history":["prod_005","prod_014","prod_016"],"purchase_history":[],"preferences":{"categories":["学生卡","团课","低价装备"],"budget":"低预算（<¥300）","goal":"减脂+社交+兴趣","level":"初级"}}];

const SG_PROMPT = `你是乐刻健身平台的AI导购助手，名字叫"小乐导购"。

## 角色
你是一个专业且有亲和力的健身产品导购。你的任务是通过对话了解用户需求，为他们推荐最合适的健身产品或课程。

## 推荐策略
1. 先了解用户的基本情况：健身经验、预算范围、健身目标
2. 根据用户的需求逐步缩小推荐范围
3. 每次推荐2-3个最匹配的产品，给出清晰的推荐理由
4. 如果用户对推荐不满意，深入了解原因，调整推荐方向
5. 尊重用户的选择，不要强行推销高价产品

## 产品类型
会员卡（¥9.9-2399）、私教课（¥59-2990）、团课（会员免费）、营养补剂（¥128-599）、运动装备（¥29-299）、线上课（¥99-365）

## 输出格式
需求明确后用格式：**推荐产品：** 1. **产品名称** - 价格 ... 推荐理由+适合人群。需求不明确时先提问。`;

const sessions = new Map();

function sseEvent(event, data) { return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`; }

async function deepseekChat(messages, temperature = 0.7, maxTokens = 2000, stream = false) {
  const resp = await fetch(DEEPSEEK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${DEEPSEEK_KEY}` },
    body: JSON.stringify({ model: MODEL, messages, temperature, max_tokens: maxTokens, stream }),
  });
  if (!resp.ok) { const err = await resp.text(); throw new Error(`DeepSeek API error ${resp.status}: ${err}`); }
  return resp;
}

async function* streamSSE(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try { const obj = JSON.parse(line.slice(6)); if (obj.choices?.[0]?.delta?.content) yield obj.choices[0].delta.content; }
        catch (e) {}
      }
    }
  }
}

function emojiForProduct(p) {
  const m = { '会员卡': '💳', '私教课': '🏋️', '团课': '🧘', '营养补剂': '💊', '运动装备': '🎽', '线上课': '📱' };
  return m[p.category] || '📦';
}

async function handleChat(body) {
  const { session_id, message, user_profile_id } = body;
  const sid = session_id || crypto.randomUUID();
  if (!sessions.has(sid)) sessions.set(sid, { history: [], type: 'sg', preferences: {} });
  const session = sessions.get(sid);
  const userMsg = message.trim();
  const profile = user_profile_id ? USER_PROFILES.find(p => p.id === user_profile_id) : null;

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      try {
        // Preference extraction
        const pp = `分析用户在健身产品导购对话中的偏好。\n消息: "${userMsg}"\n输出JSON:{"category":"会员卡/私教课/团课/营养补剂/运动装备/线上课/不确定","budget":"低/中/高/不确定","goal":"减脂/增肌/塑形/减压/康复/综合/不确定","level":"新手/有基础/资深/不确定","preferred_tags":[],"needs_clarification":true}\n只输出JSON。`;
        const pResp = await deepseekChat([{ role: 'user', content: pp }], 0.2, 300);
        let prefs = { category: '不确定', budget: '不确定', goal: '不确定', level: '不确定', preferred_tags: [], needs_clarification: true };
        try { prefs = JSON.parse((await pResp.text()).replace(/```json\n?|```/g, '').trim()); } catch (e) {}

        // Hybrid recommendations
        let recommendations = [];
        if (!prefs.needs_clarification && prefs.category !== '不确定') {
          const cfScored = PRODUCTS.map(p => {
            let s = 0;
            if (prefs.category === p.category) s += 0.3;
            for (const t of (prefs.preferred_tags || [])) if ((p.tags || []).includes(t)) s += 0.1;
            if (prefs.level === '新手' && JSON.stringify(p.target || []).match(/新手|入门|零基础/)) s += 0.15;
            if (prefs.budget === '低' && p.price < 300) s += 0.15;
            else if (prefs.budget === '中' && p.price >= 300 && p.price <= 1500) s += 0.15;
            else if (prefs.budget === '高' && p.price > 1500) s += 0.15;
            s += (p.popularity || 50) / 1000;
            if (profile?.browse_history?.includes(p.id)) s += 0.1;
            return { ...p, cf_score: s };
          });
          cfScored.sort((a, b) => b.cf_score - a.cf_score);
          const candidates = cfScored.slice(0, 15);

          const llmP = `用户偏好: 类别:${prefs.category} 预算:${prefs.budget} 目标:${prefs.goal} 水平:${prefs.level}\n候选:\n${JSON.stringify(candidates.map(c => ({ id: c.id, name: c.name, category: c.category, price: c.price, tags: c.tags, description: c.description })))}\n选出最匹配的3个产品并给出推荐理由。输出JSON数组:[{"product_id":"...","rank":1,"reason":"推荐理由","match_score":0.8}]`;
          const lResp = await deepseekChat([{ role: 'user', content: llmP }], 0.5, 500);
          let llmRanked = [];
          try { llmRanked = JSON.parse((await lResp.text()).replace(/```json\n?|```/g, '').trim()); } catch (e) {}
          if (Array.isArray(llmRanked)) {
            recommendations = llmRanked.slice(0, 3).map(item => {
              const p = PRODUCTS.find(x => x.id === item.product_id);
              if (!p) return null;
              const cfScore = cfScored.find(c => c.id === p.id)?.cf_score || 0;
              return {
                id: p.id, name: p.name, category: p.category, subcategory: p.subcategory || '',
                price: p.price, original_price: p.original_price || p.price,
                tags: p.tags || [], reason: item.reason || '',
                match_score: Math.round((0.6 * (item.match_score || 0.7) + 0.4 * cfScore) * 1000) / 1000,
                emoji: emojiForProduct(p),
              };
            }).filter(Boolean);
          }
        }

        // Pipeline
        controller.enqueue(encoder.encode(sseEvent('pipeline', {
          preferences: prefs,
          profile: profile ? { id: profile.id, name: profile.name, rfm_segment: profile.rfm_segment } : null,
          recommendations,
        })));

        // Chat
        let recCtx = '';
        if (recommendations.length) recCtx = '## 推荐结果\n' + recommendations.map((r, i) => `${i + 1}. ${r.name} - ¥${r.price} (匹配度:${Math.round(r.match_score * 100)}%) - ${r.reason}`).join('\n');
        const msgs = [
          { role: 'system', content: SG_PROMPT + '\n\n' + recCtx },
          ...session.history.slice(-20).map(h => ({ role: h.role, content: h.content })),
          { role: 'user', content: userMsg },
        ];
        const llmResp = await deepseekChat(msgs, 0.7, 1500, true);
        let full = '';
        for await (const token of streamSSE(llmResp)) {
          full += token;
          controller.enqueue(encoder.encode(sseEvent('token', { text: token })));
        }

        if (recommendations.length) controller.enqueue(encoder.encode(sseEvent('recommendations', { items: recommendations })));
        session.history.push({ role: 'user', content: userMsg }, { role: 'assistant', content: full });
        controller.enqueue(encoder.encode(sseEvent('done', { session_id: sid })));
      } catch (e) {
        controller.enqueue(encoder.encode(sseEvent('error', { message: e.message })));
      }
      controller.close();
    }
  });
  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'X-Accel-Buffering': 'no' },
  });
}

export default async function handler(req) {
  const url = new URL(req.url);
  const path = url.pathname.replace(/^\/api/, '');
  const headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type' };
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers });

  try {
    if (path === '/health') return Response.json({ status: 'ok', name: 'AI导购助手' });
    if (path === '/shopping-guide/chat' && req.method === 'POST') return handleChat(await req.json());
    if (path === '/shopping-guide/profiles') return Response.json({ profiles: USER_PROFILES });
    return new Response('Not Found', { status: 404, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { ...headers, 'Content-Type': 'application/json' } });
  }
}
