// ========================= upload.js =========================
// Handles image selection and drag & drop functionality

export function setupImageUpload({
  dropZoneId,
  inputId,
  previewContainerId,
  onFilesAdded,
}) {
  const dropZone = document.getElementById(dropZoneId);
  const fileInput = document.getElementById(inputId);
  const previewContainer = document.getElementById(previewContainerId);

  // Click to open file dialog
  dropZone.addEventListener('click', () => fileInput.click());

  // File input change
  fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

  // Drag & Drop events
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((evt) => {
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });
  ['dragenter', 'dragover'].forEach((evt) => {
    dropZone.addEventListener(evt, () => dropZone.classList.add('drag-over'));
  });
  ['dragleave', 'drop'].forEach((evt) => {
    dropZone.addEventListener(evt, () => dropZone.classList.remove('drag-over'));
  });

  dropZone.addEventListener('drop', (e) => handleFiles(e.dataTransfer.files));

  function handleFiles(files) {
    const fileList = Array.from(files);
    onFilesAdded(fileList);
  }
}