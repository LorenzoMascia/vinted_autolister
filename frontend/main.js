// ========================= main.js =========================
// Orchestrator: imports modules and initializes AutoLister class

import { setupImageUpload } from './components/upload.js';
import { setupFormValidation, validateForm } from './components/formValidator.js';
import { setupPreviewUpdater, updatePreview } from './components/previewUpdater.js';
import {
  generateAITitle,
  generateAIDescription,
  generateAIPrice,
} from './components/aiGenerator.js';
import {
  showLoadingOverlay,
  hideLoadingOverlay,
  showToast,
  animateElement,
} from './components/uiHelpers.js';