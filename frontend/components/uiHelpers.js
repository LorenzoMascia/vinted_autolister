// ========================= uiHelpers.js =========================
// Utility functions for overlays, toasts, animations

export function showLoadingOverlay({ overlayId, message }) {
  const overlay = document.getElementById(overlayId);
  if (overlay) {
    overlay.querySelector('p').textContent = message;
    overlay.classList.remove('hidden');
  }
}

export function hideLoadingOverlay(overlayId) {
  const overlay = document.getElementById(overlayId);
  overlay?.classList.add('hidden');
}

export function showToast({ toastId, message, type = 'success' }) {
  const toast = document.getElementById(toastId);
  if (!toast) return;
  // update styles based on type, e.g., bg-green or bg-red
  toast.querySelector('span').textContent = message;
  toast.classList.remove('translate-x-full');
  setTimeout(() => toast.classList.add('translate-x-full'), 4000);
}

export function animateElement(element, animationClass) {
  element.classList.add(animationClass);
  element.addEventListener(
    'animationend',
    () => element.classList.remove(animationClass),
    { once: true }
  );
}