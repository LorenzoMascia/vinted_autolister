// ========================= aiGenerator.js =========================
// Mock AI functions: replace with real API calls later

const adjectives = ['Stunning', 'Elegant', 'Stylish', 'Chic', 'Premium'];
export function generateAITitle({ category, brand, size, condition }) {
  const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
  let title = `${adj} ${brand ? brand + ' ' : ''}${category}`;
  if (size) title += ` - Size ${size}`;
  if (condition === 'new') title += ' - New with Tags';
  return title;
}

export function generateAIDescription({ category, brand, condition }) {
  let desc = `This ${category} from ${brand || 'our store'} is `;
  desc += condition === 'new' ? 'brand new with tags, ' : 'in excellent condition, ';
  desc += 'perfect for any occasion!';
  return desc;
}

export function generateAIPrice({ category, condition }) {
  const base = 20 + Math.random() * 30;
  return Math.round(base);
}