const DEEPSEEK_KEY = 'sk-d1df0d8f07fe49f9b5fe5e425ff57d86';
const DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions';
const MODEL = 'deepseek-v4-pro';

const METRICS = [{date:"2026-02-13","revenue":284500,"orders":1240,"new_users":320,"active_users":15800,"avg_order_value":229.4,"conversion_rate":0.048,"refund_rate":0.023,"satisfaction":4.3,"categories":{"会员卡":{"revenue":120000,"orders":400},"私教课":{"revenue":95000,"orders":180},"团课":{"revenue":35000,"orders":500},"商品":{"revenue":34500,"orders":160}},"channels":{"APP":0.55,"小程序":0.28,"线下":0.17}},{date:"2026-02-14","revenue":291200,"orders":1280,"new_users":345,"active_users":16100,"avg_order_value":227.5,"conversion_rate":0.049,"refund_rate":0.021,"satisfaction":4.3,"categories":{"会员卡":{"revenue":122000,"orders":410},"私教课":{"revenue":98000,"orders":185},"团课":{"revenue":36200,"orders":520},"商品":{"revenue":35000,"orders":165}},"channels":{"APP":0.56,"小程序":0.27,"线下":0.17}},{date:"2026-02-15","revenue":275000,"orders":1190,"new_users":280,"active_users":15200,"avg_order_value":231.1,"conversion_rate":0.046,"refund_rate":0.025,"satisfaction":4.2,"categories":{"会员卡":{"revenue":115000,"orders":385},"私教课":{"revenue":92000,"orders":170},"团课":{"revenue":34000,"orders":480},"商品":{"revenue":34000,"orders":155}},"channels":{"APP":0.54,"小程序":0.28,"线下":0.18}},{date:"2026-02-16","revenue":289800,"orders":1260,"new_users":310,"active_users":15900,"avg_order_value":230,"conversion_rate":0.048,"refund_rate":0.022,"satisfaction":4.3,"categories":{"会员卡":{"revenue":124000,"orders":415},"私教课":{"revenue":95000,"orders":178},"团课":{"revenue":35800,"orders":510},"商品":{"revenue":35000,"orders":157}},"channels":{"APP":0.55,"小程序":0.28,"线下":0.17}},{date:"2026-02-17","revenue":302000,"orders":1320,"new_users":350,"active_users":16400,"avg_order_value":228.8,"conversion_rate":0.05,"refund_rate":0.02,"satisfaction":4.4,"categories":{"会员卡":{"revenue":128000,"orders":430},"私教课":{"revenue":102000,"orders":195},"团课":{"revenue":37000,"orders":530},"商品":{"revenue":35000,"orders":165}},"channels":{"APP":0.57,"小程序":0.26,"线下":0.17}},{date:"2026-02-18","revenue":315000,"orders":1380,"new_users":380,"active_users":16800,"avg_order_value":228.3,"conversion_rate":0.052,"refund_rate":0.019,"satisfaction":4.4,"categories":{"会员卡":{"revenue":135000,"orders":450},"私教课":{"revenue":105000,"orders":200},"团课":{"revenue":39000,"orders":560},"商品":{"revenue":36000,"orders":170}},"channels":{"APP":0.58,"小程序":0.25,"线下":0.17}},{date:"2026-02-19","revenue":298000,"orders":1300,"new_users":340,"active_users":16200,"avg_order_value":229.2,"conversion_rate":0.049,"refund_rate":0.021,"satisfaction":4.3,"categories":{"会员卡":{"revenue":126000,"orders":420},"私教课":{"revenue":98000,"orders":185},"团课":{"revenue":38000,"orders":540},"商品":{"revenue":36000,"orders":155}},"channels":{"APP":0.56,"小程序":0.27,"线下":0.17}},{date:"2026-02-20","revenue":308000,"orders":1340,"new_users":360,"active_users":16500,"avg_order_value":229.9,"conversion_rate":0.051,"refund_rate":0.02,"satisfaction":4.3,"categories":{"会员卡":{"revenue":130000,"orders":435},"私教课":{"revenue":100000,"orders":190},"团课":{"revenue":40000,"orders":555},"商品":{"revenue":38000,"orders":160}},"channels":{"APP":0.57,"小程序":0.26,"线下":0.17}},{date:"2026-02-21","revenue":322000,"orders":1410,"new_users":395,"active_users":17000,"avg_order_value":228.4,"conversion_rate":0.053,"refund_rate":0.018,"satisfaction":4.5,"categories":{"会员卡":{"revenue":138000,"orders":460},"私教课":{"revenue":108000,"orders":208},"团课":{"revenue":40000,"orders":570},"商品":{"revenue":36000,"orders":172}},"channels":{"APP":0.58,"小程序":0.25,"线下":0.17}},{date:"2026-02-22","revenue":310000,"orders":1350,"new_users":370,"active_users":16700,"avg_order_value":229.6,"conversion_rate":0.05,"refund_rate":0.02,"satisfaction":4.3,"categories":{"会员卡":{"revenue":132000,"orders":440},"私教课":{"revenue":102000,"orders":195},"团课":{"revenue":39000,"orders":555},"商品":{"revenue":37000,"orders":160}},"channels":{"APP":0.57,"小程序":0.26,"线下":0.17}},{date:"2026-03-01","revenue":318000,"orders":1390,"new_users":385,"active_users":17100,"avg_order_value":228.8,"conversion_rate":0.052,"refund_rate":0.018,"satisfaction":4.5,"categories":{"会员卡":{"revenue":138000,"orders":460},"私教课":{"revenue":108000,"orders":205},"团课":{"revenue":38000,"orders":560},"商品":{"revenue":34000,"orders":165}},"channels":{"APP":0.58,"小程序":0.25,"线下":0.17}},{date:"2026-03-05","revenue":309000,"orders":1350,"new_users":365,"active_users":16700,"avg_order_value":228.9,"conversion_rate":0.05,"refund_rate":0.02,"satisfaction":4.4,"categories":{"会员卡":{"revenue":132000,"orders":440},"私教课":{"revenue":105000,"orders":200},"团课":{"revenue":38000,"orders":550},"商品":{"revenue":34000,"orders":160}},"channels":{"APP":0.57,"小程序":0.26,"线下":0.17}},{date:"2026-03-08","revenue":340000,"orders":1490,"new_users":430,"active_users":17900,"avg_order_value":228.2,"conversion_rate":0.055,"refund_rate":0.017,"satisfaction":4.5,"categories":{"会员卡":{"revenue":150000,"orders":500},"私教课":{"revenue":115000,"orders":220},"团课":{"revenue":39000,"orders":600},"商品":{"revenue":36000,"orders":170}},"channels":{"APP":0.59,"小程序":0.24,"线下":0.17}},{date:"2026-03-12","revenue":298000,"orders":1295,"new_users":325,"active_users":16000,"avg_order_value":230.1,"conversion_rate":0.048,"refund_rate":0.022,"satisfaction":4.2,"categories":{"会员卡":{"revenue":125000,"orders":418},"私教课":{"revenue":96000,"orders":182},"团课":{"revenue":40000,"orders":540},"商品":{"revenue":37000,"orders":155}},"channels":{"APP":0.55,"小程序":0.28,"线下":0.17}}];

async function deepseekChat(messages, temperature = 0.7, maxTokens = 2000, stream = false) {
  const resp = await fetch(DEEPSEEK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${DEEPSEEK_KEY}` },
    body: JSON.stringify({ model: MODEL, messages, temperature, max_tokens: maxTokens, stream }),
  });
  if (!resp.ok) { const err = await resp.text(); throw new Error(`DeepSeek API error ${resp.status}: ${err}`); }
  return resp;
}

function handleMetrics() {
  const today = METRICS[METRICS.length - 1];
  const yesterday = METRICS[METRICS.length - 2] || today;
  return Response.json({
    date: today.date, revenue: today.revenue, orders: today.orders, new_users: today.new_users,
    active_users: today.active_users, avg_order_value: today.avg_order_value,
    conversion_rate: today.conversion_rate, refund_rate: today.refund_rate, satisfaction: today.satisfaction,
    deltas: {
      revenue: Math.round((today.revenue - yesterday.revenue) / yesterday.revenue * 1000) / 10,
      orders: Math.round((today.orders - yesterday.orders) / yesterday.orders * 1000) / 10,
      new_users: Math.round((today.new_users - yesterday.new_users) / yesterday.new_users * 1000) / 10,
      conversion_rate: Math.round((today.conversion_rate - yesterday.conversion_rate) * 10000) / 100,
      avg_order_value: Math.round((today.avg_order_value - yesterday.avg_order_value) / yesterday.avg_order_value * 1000) / 10,
    },
    categories: today.categories, channels: today.channels,
  });
}

function handleChartData(type) {
  const recent = METRICS.slice(-30);
  if (type === 'revenue_trend') return Response.json({ x: recent.map(m => m.date), series: [{ name: '营收', data: recent.map(m => m.revenue) }] });
  if (type === 'category_pie') {
    const today = METRICS[METRICS.length - 1];
    return Response.json({ data: Object.entries(today.categories).map(([k, v]) => ({ name: k, value: v.revenue })) });
  }
  if (type === 'user_growth') return Response.json({ x: recent.map(m => m.date), series: [{ name: '新用户', data: recent.map(m => m.new_users) }, { name: '活跃(÷100)', data: recent.map(m => Math.round(m.active_users / 100)) }] });
  if (type === 'conversion_funnel') return Response.json({ labels: ['浏览', '加购', '下单', '支付'], data: [8500, 2400, 1380, 1240] });
  return Response.json({ x: [], series: [] });
}

function handleAlerts() {
  if (METRICS.length < 8) return Response.json([]);
  const today = METRICS[METRICS.length - 1];
  const window = METRICS.slice(-8, -1);
  const alerts = [];
  for (const [field, name] of [['revenue', '营收'], ['orders', '订单数'], ['new_users', '新用户数'], ['refund_rate', '退款率'], ['conversion_rate', '转化率']]) {
    const values = window.map(m => m[field]);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const std = Math.sqrt(values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length);
    if (std === 0) continue;
    const z = (today[field] - mean) / std;
    if (Math.abs(z) > 2) alerts.push({ field, name, current: today[field], mean_7d: Math.round(mean * 100) / 100, z_score: Math.round(z * 100) / 100, direction: z > 0 ? '上升' : '下降', severity: Math.abs(z) > 3 ? 'critical' : 'warning' });
  }
  return Response.json(alerts);
}

async function handleDailySummary() {
  const today = METRICS[METRICS.length - 1];
  // Build alerts
  const win = METRICS.slice(-8, -1);
  let alertText = '';
  for (const [field, name] of [['revenue','营收'],['orders','订单数'],['new_users','新用户数'],['refund_rate','退款率'],['conversion_rate','转化率']]) {
    const values = win.map(m => m[field]);
    const mean = values.reduce((a,b)=>a+b,0)/values.length;
    const std = Math.sqrt(values.reduce((s,v)=>s+(v-mean)**2,0)/values.length);
    if (std > 0) { const z = (today[field]-mean)/std; if (Math.abs(z)>2) alertText += `- ${name}异常${z>0?'上升':'下降'}: 当前${today[field]}, 7日均值${Math.round(mean*100)/100}\n`; }
  }

  const prompt = `根据以下数据生成健身连锁企业经营日报（300-500字）。\n日期: ${today.date}\n营收: ¥${today.revenue.toLocaleString()}\n订单数: ${today.orders}\n新用户: ${today.new_users}\n客单价: ¥${today.avg_order_value}\n转化率: ${(today.conversion_rate*100).toFixed(1)}%\n退款率: ${(today.refund_rate*100).toFixed(1)}%\n满意度: ${today.satisfaction}/5.0\n品类: ${JSON.stringify(today.categories)}\n${alertText ? '异常提醒:\n'+alertText : ''}\n\n要求: 1-2句概括; 分品类简析; 指出亮点/问题; 1-2条建议; 300-500字; 专业但可读。`;
  const resp = await deepseekChat([{ role: 'user', content: prompt }], 0.4, 1000);
  const report = await resp.text();
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < report.length; i += 20) {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify({ text: report.slice(i, i + 20) })}\n\n`));
      }
      controller.enqueue(encoder.encode(`data: ${JSON.stringify({ done: true, full: report })}\n\n`));
      controller.close();
    }
  });
  return new Response(stream, { headers: { 'Content-Type': 'text/event-stream' } });
}

async function handleNLQuery(body) {
  const { query } = body;
  const recent = METRICS.slice(-7);
  const p = `数据库: daily_metrics (date, revenue, orders, new_users, active_users, avg_order_value, conversion_rate, refund_rate, satisfaction)\n最近7天数据: ${JSON.stringify(recent.map(m=>({date:m.date,revenue:m.revenue,orders:m.orders,new_users:m.new_users,conversion_rate:m.conversion_rate})))}\n查询: "${query}"\n分析回答(100-200字)。输出JSON:{"type":"summary/trend/ranking/anomaly/fact","answer":"分析回答","insight":"关键洞察(1句话,可为null)"}\n只输出JSON。`;
  const resp = await deepseekChat([{ role: 'user', content: p }], 0.1, 500);
  let result = { type: 'fact', answer: '暂无分析结果', insight: null };
  try { result = JSON.parse((await resp.text()).replace(/```json\n?|```/g, '').trim()); } catch (e) {}
  result.recent_data = recent.map(m => ({ date: m.date, revenue: m.revenue, orders: m.orders, new_users: m.new_users, conversion_rate: m.conversion_rate }));
  return Response.json(result);
}

export default async function handler(req) {
  const url = new URL(req.url);
  const path = url.pathname.replace(/^\/api/, '');
  const headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type' };
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers });

  try {
    if (path === '/health') return Response.json({ status: 'ok', name: 'AI数据驾驶舱' });
    if (path === '/data-cockpit/metrics') return handleMetrics();
    if (path === '/data-cockpit/weekly-trend') return Response.json(METRICS.slice(-7));
    if (path.startsWith('/data-cockpit/chart-data/')) return handleChartData(path.split('/').pop());
    if (path === '/data-cockpit/alerts') return handleAlerts();
    if (path === '/data-cockpit/daily-summary') return handleDailySummary();
    if (path === '/data-cockpit/nl-query' && req.method === 'POST') return handleNLQuery(await req.json());
    return new Response('Not Found', { status: 404, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { ...headers, 'Content-Type': 'application/json' } });
  }
}
