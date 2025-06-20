// ========================= previewUpdater.js =========================
// Updates live preview based on form input and images

export function setupPreviewUpdater({
  inputIds = [],
  previewIds = {},
  getState,
}) {
  inputIds.forEach((id) => {
    const el = document.getElementById(id);
    el?.addEventListener('input', () => updatePreview({ previewIds, getState }));
  });
}

export function updatePreview({ previewIds, getState }) {
  const {
    title,
    description,
    price,
    categoryText,
    size,
    conditionText,
    images,
    currentImageIndex,
  } = getState();

  // Text fields
  document.getElementById(previewIds.title).textContent = title || 'Your Amazing Item';
  document.getElementById(previewIds.description).textContent = description || 'Describe your item...';
  document.getElementById(previewIds.price).textContent = price ? `€${parseFloat(price).toFixed(2)}` : '€0.00';

  // Tags
  const setTag = (id, text) => {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = text;
      el.style.display = text ? 'inline-block' : 'none';
    }
  };
  setTag(previewIds.category, categoryText);
  setTag(previewIds.size, size ? `Size: ${size.toUpperCase()}` : '');
  setTag(previewIds.condition, conditionText);

  // Image
  const imgEl = document.querySelector(`#${previewIds.image} img`);
  if (imgEl && images.length > 0) {
    imgEl.src = images[currentImageIndex].url;
    imgEl.alt = images[currentImageIndex].name;
  }
}
