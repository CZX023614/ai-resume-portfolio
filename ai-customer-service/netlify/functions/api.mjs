const DEEPSEEK_KEY = 'sk-d1df0d8f07fe49f9b5fe5e425ff57d86';
const DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions';
const MODEL = 'deepseek-v4-pro';

const FAQ_KB = [{id:"faq_001","category":"会员卡","question":"如何购买会员卡？","keywords":["购买","会员卡","办卡","开通","怎么买"],"answer":"您可以在乐刻APP首页点击「会员卡」入口，选择您想要的卡种（月卡/季卡/年卡/体验卡），点击「立即购买」完成支付即可开通。支付方式支持微信、支付宝、银行卡。购买后即时生效，可在「我的-会员卡」查看。"},{id:"faq_002","category":"会员卡","question":"会员卡可以退款吗？","keywords":["退款","退卡","退费","取消会员"],"answer":"会员卡购买7天内且未使用可全额退款。已使用的会员卡按剩余天数折算退费：退款金额=支付金额÷总天数×剩余天数×80%（扣除20%手续费）。退款路径：APP「我的」→「会员卡」→「申请退款」→填写原因→1-3个工作日到账。"},{id:"faq_003","category":"会员卡","question":"不同类型的会员卡有什么区别？","keywords":["月卡","季卡","年卡","体验卡","区别","哪种","卡种"],"answer":"乐刻提供四种会员卡：1)月卡¥299/月，灵活按月续费；2)季卡¥799/季(省¥98)；3)年卡¥2399/年(省¥1189)，性价比最高；4)7天体验卡¥9.9，仅限新用户首次购买。所有卡种均可全城通用、不限次数。"},{id:"faq_004","category":"会员卡","question":"退款多久到账？","keywords":["退款","到账","时间","多久","进度"],"answer":"退款审核通过后：微信/支付宝支付1-3个工作日到账，银行卡支付3-5个工作日到账。审核周期1-2个工作日。您可以在APP「我的-退款记录」中查看进度。如超过5个工作日仍未到账，请联系客服。"},{id:"faq_005","category":"会员卡","question":"会员卡可以转让吗？","keywords":["转让","给别人","转卡"],"answer":"会员卡不支持转让。每张会员卡与购买账户绑定，仅限本人使用。门店入场需扫码验证身份，非本人无法使用。如果需要给朋友办理，可以推荐朋友购买体验卡或使用「邀请有礼」功能。"},{id:"faq_006","category":"会员卡","question":"会员卡快到期了怎么续费？","keywords":["续费","到期","续卡","继续"],"answer":"APP「我的」→「会员卡」→点击「续费」按钮即可续费。续费不改变原卡到期规则，在原到期日后顺延。续费同样享受会员价，到期前7天系统会发送提醒。开通自动续费可享9折优惠。"},{id:"faq_007","category":"会员卡","question":"体验卡和正式会员卡有什么区别？","keywords":["体验卡","9.9","新手","试用"],"answer":"7天体验卡（¥9.9）仅限新用户首次购买，有效期内无限次使用，7天后自动失效不自动续费。体验卡到期后可购买正式会员卡。体验卡不支持退款。每个手机号限购1次。"},{id:"faq_008","category":"会员卡","question":"什么情况下不能退款？","keywords":["不能退款","退款条件","退不了"],"answer":"以下情况不支持退款：1)购买超过7天；2)已使用超过3次；3)体验卡(¥9.9)不支持退款；4)通过活动赠送的会员天数；5)已申请过退款的订单（不支持重复退款）。"},{id:"faq_009","category":"约课","question":"怎么预约团课？","keywords":["预约","团课","约课","上课","预订"],"answer":"APP首页点击「团课」→选择门店→选择课程→点击「预约」。课程提前3天放出，热门课程建议准点抢课。每人每天最多预约3节课。预约后未签到将被视为爽约，累计3次将限制预约功能7天。"},{id:"faq_010","category":"约课","question":"预约的课怎么取消？","keywords":["取消","预约","退课","不去"],"answer":"在APP「我的-我的预约」中找到对应课程，点击「取消预约」。开课前2小时可自由取消。开课前2小时内取消记爽约1次。累计爽约3次将限制预约功能7天。"},{id:"faq_011","category":"约课","question":"预约满了怎么办？排队等候是什么？","keywords":["满了","排队","等候","没位置","候补"],"answer":"课满后可点击「排队等候」进入候补队列。有人取消，系统按排队顺序自动预约并推送通知。排上后需在30分钟内确认，超时视为放弃。建议同时关注其他时段同类型课程。"},{id:"faq_012","category":"约课","question":"私教课怎么预约？","keywords":["私教","一对一","教练","预约"],"answer":"APP首页「私教」→选择教练→查看教练简介和擅长领域→选择时间段→支付→预约成功。私教课需提前24小时预约。第一次上课建议先购买单次体验课（¥99），满意后再购买课包。"},{id:"faq_015","category":"门店","question":"怎么找到离我最近的门店？","keywords":["门店","最近","附近","地址","导航"],"answer":"APP首页自动定位→显示附近门店列表（按距离排序）→点击可查看门店详情（地址/营业时间/设施/课程表/当前人数）。支持地图模式查看分布。全国覆盖40+城市、2000+门店。"},{id:"faq_016","category":"门店","question":"门店的营业时间是？","keywords":["营业时间","几点开门","几点关门","时间"],"answer":"标准门店营业时间为6:00-24:00（部分商场店随商场时间调整，通常为10:00-22:00）。春节期间营业时间可能有调整，请关注APP公告。24小时门店正在逐步开放中。"},{id:"faq_017","category":"门店","question":"门店有哪些设施？","keywords":["设施","设备","淋浴","更衣室","wifi"],"answer":"乐刻标配设施包括：有氧区（跑步机/椭圆机/划船机）、力量区（哑铃/杠铃/龙门架/史密斯机）、操房、更衣室、淋浴间（提供洗发水/沐浴露）、储物柜（自带锁或扫码）。部分大型门店设有搏击区、攀岩墙。"},{id:"faq_018","category":"私教","question":"私教课怎么收费？","keywords":["私教","价格","费用","多少钱","收费"],"answer":"私教课价格因教练级别而异：初级教练¥199-299/节，高级教练¥299-399/节，明星教练¥399-599/节。首次体验课统一¥99/节。课包购买更优惠：10节包9折、20节包8.5折、50节包8折。"},{id:"faq_020","category":"账户","question":"怎么修改绑定的手机号？","keywords":["换手机号","修改手机","绑定","更换"],"answer":"APP「我的」→「设置」→「账号安全」→「修改手机号」→验证原手机号→绑定新手机号→完成。如果原手机号已无法接收验证码，需联系在线客服进行人工审核换绑。"},{id:"faq_021","category":"账户","question":"忘记密码怎么办？","keywords":["忘记密码","找回","重置","登录不了"],"answer":"在登录页面点击「忘记密码」→输入注册手机号→接收验证码→设置新密码→完成。如未收到验证码，请检查短信是否被拦截，或联系客服。"},{id:"faq_022","category":"账户","question":"账号被冻结了怎么办？","keywords":["冻结","封号","账号异常","不能登录"],"answer":"账号冻结多见于以下原因：1)异常登录保护（异地登录）；2)违规使用（如账号共享/外挂打卡）；3)支付风险。解冻方式：APP内按提示进行身份验证，或联系在线客服人工处理。"},{id:"faq_023","category":"活动","question":"最近有什么优惠活动？","keywords":["优惠","活动","促销","折扣","便宜"],"answer":"当前活动：1)新用户注册领¥50优惠券；2)邀请好友办卡各得7天会员；3)会员日每月18号限时秒杀；4)学生认证享年卡8折；5)企业团购10人以上享专属优惠。"},{id:"faq_025","category":"活动","question":"学生有优惠吗？","keywords":["学生","优惠","学生价","认证"],"answer":"全日制在校大学生完成学生认证后，可享年卡8折优惠（¥1919/年，原价¥2399）。认证方式：APP「我的」→「学生认证」→上传学生证照片→审核1-2个工作日。每年需重新认证。"},{id:"faq_028","category":"门店","question":"门店人多吗？怎么避开高峰期？","keywords":["人多","高峰期","拥挤","什么时候人少"],"answer":"APP门店详情页可查看实时在场人数。高峰期一般为：工作日17:30-20:30、周末10:00-12:00及15:00-17:00。低谷期为：工作日6:00-9:00、13:00-16:00、21:00-24:00。建议避开高峰时段。"},{id:"faq_031","category":"其他","question":"APP闪退/卡顿怎么办？","keywords":["闪退","卡顿","崩溃","bug","不好用"],"answer":"尝试以下步骤：1)更新APP至最新版本；2)清除APP缓存（设置→通用→清除缓存）；3)重启手机；4)卸载重装APP（注意备份数据）。如问题持续，请在APP「设置-意见反馈」提交机型和使用场景。"}];

const CS_PROMPT = `你是乐刻健身平台的AI智能客服助手，名字叫"小乐"。

## 角色
你是一个友好、专业、耐心的客服助手。你需要帮助用户解决关于乐刻健身平台的问题。

## 知识范围
会员卡：购买、续费、升级、退款、卡种区别。约课：团课预约、取消、排队等候、私教预约。门店：地址查询、营业时间、设施。账户：注册、登录、密码找回、注销。活动：优惠、邀请好友、学生优惠。退款：退款条件、退款流程、到账时间。

## 行为规则
1. 先确认用户意图，再给出回答
2. 回答应基于提供的知识库内容，不要编造信息
3. 如果知识库中没有相关信息，建议用户联系人工客服
4. 回复简洁明了，控制在200字以内
5. 涉及退款、投诉等敏感问题，语气需格外温和
6. 使用中文，语气亲切但不啰嗦`;

const sessions = new Map();

function tokenize(text) {
  const words = [];
  const re = /[一-鿿]+|[a-z0-9]+/g;
  let m;
  while ((m = re.exec(text.toLowerCase())) !== null) {
    words.push(m[0]);
    if (/[一-鿿]/.test(m[0])) for (let i = 0; i < m[0].length - 1; i++) words.push(m[0].slice(i, i + 2));
  }
  return words;
}

function ragSearch(query, topK = 5) {
  const queryTokens = tokenize(query);
  const qSet = new Set(queryTokens);
  const results = FAQ_KB.map(entry => {
    const docText = entry.question + ' ' + (entry.keywords || []).join(' ') + ' ' + entry.answer;
    const docTokens = tokenize(docText);
    let score = 0;
    for (const t of qSet) { const cnt = docTokens.filter(d => d === t).length; if (cnt > 0) score += cnt; }
    for (const kw of (entry.keywords || [])) { if (query.includes(kw)) score += 1.5; }
    return { entry, score };
  });
  results.sort((a, b) => b.score - a.score);
  const maxScore = results[0]?.score || 1;
  return results.slice(0, topK).map(r => ({
    id: r.entry.id, category: r.entry.category, question: r.entry.question, answer: r.entry.answer,
    score: maxScore > 0 ? Math.round((r.score / maxScore) * 1000) / 1000 : 0,
  }));
}

async function deepseekChat(messages, temperature = 0.7, maxTokens = 2000, stream = false) {
  const resp = await fetch(DEEPSEEK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${DEEPSEEK_KEY}` },
    body: JSON.stringify({ model: MODEL, messages, temperature, max_tokens: maxTokens, stream }),
  });
  if (!resp.ok) { const err = await resp.text(); throw new Error(`DeepSeek API error ${resp.status}: ${err}`); }
  return resp;
}

function sseEvent(event, data) { return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`; }

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

async function handleChat(body) {
  const { session_id, message } = body;
  const sid = session_id || crypto.randomUUID();
  if (!sessions.has(sid)) sessions.set(sid, { history: [], type: 'cs' });
  const session = sessions.get(sid);
  const userMsg = message.trim();

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      try {
        // Intent classification
        const ip = `分析用户发给健身平台AI客服的这句话，输出JSON。\n用户消息: "${userMsg}"\n输出JSON:{"intent":"会员卡/约课/门店/账户/退款/活动/其他","sub_intent":"...","entities":[],"confidence":0.8,"sentiment":"neutral"}\n只输出JSON。`;
        const iResp = await deepseekChat([{ role: 'user', content: ip }], 0.1, 200);
        let intentData = { intent: '其他', sub_intent: '', entities: [], confidence: 0.7, sentiment: 'neutral' };
        try { intentData = JSON.parse((await iResp.text()).replace(/```json\n?|```/g, '').trim()); } catch (e) {}

        // RAG
        const ragResults = ragSearch(userMsg);
        const topScore = ragResults[0]?.score || 0;

        // Confidence
        const conf = {
          score: Math.round(Math.max(0, Math.min(1, (intentData.confidence || 0.7) + (ragResults.length >= 3 && topScore > 0.7 ? 0.05 : -0.1))) * 1000) / 1000,
          level: '', auto_handoff: false,
        };
        conf.level = conf.score >= 0.85 ? 'high' : (conf.score >= 0.75 ? 'medium' : 'low');
        conf.auto_handoff = conf.score < 0.75;

        // Pipeline
        controller.enqueue(encoder.encode(sseEvent('pipeline', {
          intent: intentData.intent, sub_intent: intentData.sub_intent || '', entities: intentData.entities || [],
          sentiment: intentData.sentiment || 'neutral',
          rag_sources: ragResults.slice(0, 3).map(r => ({ category: r.category, question: r.question, score: r.score })),
          confidence: conf,
        })));

        // Chat
        const ragCtx = ragResults.slice(0, 3).map((r, i) => `[条目${i + 1}] ${r.category} | ${r.question}\n答案: ${r.answer}`).join('\n');
        const msgs = [
          { role: 'system', content: CS_PROMPT + `\n\n## 参考知识库\n${ragCtx}` },
          ...session.history.slice(-20).map(h => ({ role: h.role, content: h.content })),
          { role: 'user', content: userMsg },
        ];
        const llmResp = await deepseekChat(msgs, 0.3, 1000, true);
        let full = '';
        for await (const token of streamSSE(llmResp)) {
          full += token;
          controller.enqueue(encoder.encode(sseEvent('token', { text: token })));
        }

        controller.enqueue(encoder.encode(sseEvent('confidence', conf)));
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
    if (path === '/health') return Response.json({ status: 'ok', name: 'AI智能客服系统' });
    if (path === '/customer-service/chat' && req.method === 'POST') return handleChat(await req.json());
    return new Response('Not Found', { status: 404, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { ...headers, 'Content-Type': 'application/json' } });
  }
}
