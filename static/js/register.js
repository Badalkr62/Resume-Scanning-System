// ==========================================
// REGISTER ENGINE & INTERACTION UTILITIES
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
  
  // 1. PAGE FADE-IN ENGINE
  document.body.style.opacity = "1";

  // 2. TOGGLE PASSWORD EYE REFRACTOR
  const passwordField = document.querySelector('input[name="password"]');
  const toggleVisibilityBtn = document.getElementById("togglePassword");

  if (toggleVisibilityBtn && passwordField) {
    toggleVisibilityBtn.addEventListener("click", function () {
      const isSensitive = passwordField.getAttribute("type") === "password";
      passwordField.setAttribute("type", isSensitive ? "text" : "password");
      
      this.innerHTML = isSensitive 
        ? '<i class="fa-solid fa-eye-slash"></i>' 
        : '<i class="fa-solid fa-eye"></i>';
    });
  }

  // 3. ASYNC FORM INTERCEPTION & LOADING SPINNER
  const registrationForm = document.querySelector("form");
  const actionButton = document.querySelector(".login-btn");

  if (registrationForm && actionButton) {
    registrationForm.addEventListener("submit", function () {
      actionButton.disabled = true;
      actionButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Creating Account...
      `;
    });
  }

  // 4. METRIC TILT ROTATION SYSTEM (3D TILT EFFECT)
  const structuralCard = document.querySelector(".login-card");
  if (structuralCard && window.innerWidth > 992) {
    structuralCard.addEventListener("mousemove", function (e) {
      const dimensionRect = structuralCard.getBoundingClientRect();
      const cursorX = e.clientX - dimensionRect.left;
      const cursorY = e.clientY - dimensionRect.top;

      const tiltDegreeX = -(cursorY - dimensionRect.height / 2) / 25;
      const tiltDegreeY = (cursorX - dimensionRect.width / 2) / 25;

      structuralCard.style.transform = `rotateX(${tiltDegreeX}deg) rotateY(${tiltDegreeY}deg) `;
    });

    structuralCard.addEventListener("mouseleave", function () {
      structuralCard.style.transform = "rotateX(0deg) rotateY(0deg)";
    });
  }

  // 5. AMBIENT GLOW SYSTEM FOR INPUT GROUPS
  document.querySelectorAll(".form-control, .form-select").forEach((inputNode) => {
    const structuralContainer = inputNode.parentElement;
    
    // Check if fields are encased inside bootstrap input groups
    const targetElement = structuralContainer.classList.contains("input-group") 
      ? structuralContainer 
      : inputNode;

    inputNode.addEventListener("focus", () => {
      targetElement.style.borderColor = "#6c4cff";
      targetElement.style.boxShadow = "0 0 15px rgba(108, 76, 255, 0.4)";
    });

    inputNode.addEventListener("blur", () => {
      targetElement.style.borderColor = "#222f54";
      targetElement.style.boxShadow = "none";
    });
  });

  // 6. BACKGROUND SKY PARTICLES DISPATCHER
  function generateParticle() {
    const lightSpot = document.createElement("span");
    lightSpot.classList.add("particle");

    lightSpot.style.left = Math.random() * window.innerWidth + "px";
    lightSpot.style.animationDuration = Math.random() * 5 + 5 + "s";
    lightSpot.style.opacity = Math.random() * 0.7 + 0.2;

    const diameterSize = Math.random() * 6 + 3 + "px";
    lightSpot.style.width = diameterSize;
    lightSpot.style.height = diameterSize;

    document.body.appendChild(lightSpot);

    setTimeout(() => {
      lightSpot.remove();
    }, 9000);
  }
  setInterval(generateParticle, 400);
});

// ==========================================
// REGISTER PASSWORD SHOW / HIDE FIX
// ==========================================
const registerPassword = document.getElementById("registerPassword");
const toggleRegisterPassword = document.getElementById("toggleRegisterPassword");

if (registerPassword && toggleRegisterPassword) {
  toggleRegisterPassword.addEventListener("click", function () {
    // टाइप चेक करें और बदलें
    const isPassword = registerPassword.type === "password";
    registerPassword.type = isPassword ? "text" : "password";

    // आइकॉन को बदलें
    this.innerHTML = isPassword 
      ? '<i class="fa-solid fa-eye-slash"></i>' 
      : '<i class="fa-solid fa-eye"></i>';
  });
}