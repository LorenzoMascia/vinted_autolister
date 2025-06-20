// ========================= formValidator.js =========================
// Validates individual fields and overall form before actions

export function setupFormValidation({
  requiredFieldIds = [],
  onValidationError,
}) {
  requiredFieldIds.forEach((id) => {
    const field = document.getElementById(id);
    field?.addEventListener('blur', () => validateField(field, onValidationError));
  });
}

export function validateField(field, onError) {
  const value = field.value.trim();
  let error = '';

  if (!value) {
    error = 'This field is required';
  } else if (field.type === 'number' && parseFloat(value) <= 0) {
    error = 'Please enter a valid number';
  } else if (field.id === 'title-input' && value.length < 10) {
    error = 'Title must be at least 10 characters';
  } else if (field.id === 'description-input' && value.length < 20) {
    error = 'Description must be at least 20 characters';
  }

  if (error) {
    onError(field, error);
    return false;
  }
  return true;
}

export function validateForm({
  requiredFieldIds = [],
  uploadedImages = [],
  onError,
}) {
  let isValid = true;
  if (uploadedImages.length === 0) {
    onError(null, 'Please upload at least one image');
    isValid = false;
  }
  requiredFieldIds.forEach((id) => {
    const field = document.getElementById(id);
    if (field && !validateField(field, onError)) {
      isValid = false;
    }
  });
  return isValid;
}
