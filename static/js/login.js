// ==========================================
// CLIENT RUNTIME INTERACTION - LOGIN ENGINE
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
  // 1. PAGE FADE IN EFFECT ON LOAD
  document.body.style.opacity = "1";

  // 2. PASSWORD VISIBILITY TOGGLE WITH ICON SWITCH
  const passwordInput = document.getElementById("password");
  const togglePasswordBtn = document.getElementById("togglePassword");

  if (passwordInput && togglePasswordBtn) {
    togglePasswordBtn.addEventListener("click", function () {
      const isHidden = passwordInput.type === "password";
      passwordInput.type = isHidden ? "text" : "password";
      this.innerHTML = isHidden
        ? '<i class="fa-solid fa-eye-slash"></i>'
        : '<i class="fa-solid fa-eye"></i>';
    });
  }

  // 3. SECURE FORM SUBMIT & ASYNC BUTTON SPINNING LOADER
  const loginForm = document.querySelector("form");
  const loginBtn = document.querySelector(".login-btn");

  if (loginForm && loginBtn) {
    loginForm.addEventListener("submit", () => {
      loginBtn.disabled = true;
      loginBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Signing In Securely...
            `;
    });
  }

  // 4. DIGITAL CLOCK ENGINE (TIMEZONE STABLE)
  function updateClock() {
    const clockContainer = document.getElementById("clock");
    if (clockContainer) {
      const localDate = new Date();
      clockContainer.innerHTML = localDate.toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
    }
  }
  setInterval(updateClock, 1000);
  updateClock(); // Initial Trigger

  // 5. ENHANCED TYPING EFFECT GENERATOR
  const textQueue = ["Welcome Back!", "Secure Dashboard", "Connect & Grow 🚀"];
  let queueIndex = 0;
  let charIndex = 0;
  let removing = false;
  const typingTarget = document.getElementById("typing");

  function executeTyping() {
    if (!typingTarget) return;
    const currentString = textQueue[queueIndex];

    if (removing) {
      typingTarget.innerText = currentString.substring(0, charIndex - 1);
      charIndex--;
    } else {
      typingTarget.innerText = currentString.substring(0, charIndex + 1);
      charIndex++;
    }

    let pace = removing ? 40 : 80;

    if (!removing && charIndex === currentString.length) {
      pace = 2000; // Standstill delay
      removing = true;
    } else if (removing && charIndex === 0) {
      removing = false;
      queueIndex = (queueIndex + 1) % textQueue.length;
      pace = 400; // Interval change wait
    }
    setTimeout(executeTyping, pace);
  }
  executeTyping();

  // 6. MATRICES GLOW BINDING FOR INPUT GROUPS
  document.querySelectorAll(".form-control").forEach((inputField) => {
    const structuralParent = inputField.parentElement;
    if (
      structuralParent &&
      structuralParent.classList.contains("input-group")
    ) {
      inputField.addEventListener("focus", () => {
        structuralParent.style.borderColor = "#6c4cff";
        structuralParent.style.boxShadow = "0 0 15px rgba(108, 76, 255, 0.4)";
      });
      inputField.addEventListener("blur", () => {
        structuralParent.style.borderColor = "#222f54";
        structuralParent.style.boxShadow = "none";
      });
    }
  });

  // 7. GYROSCOPIC INTERACTIVE CARD 3D EFFECT
  const functionalCard = document.querySelector(".login-card");
  if (functionalCard && window.innerWidth > 992) {
    functionalCard.addEventListener("mousemove", (event) => {
      const boundaries = functionalCard.getBoundingClientRect();
      const axisX = event.clientX - boundaries.left;
      const axisY = event.clientY - boundaries.top;

      const inclinationX = -(axisY - boundaries.height / 2) / 25;
      const inclinationY = (axisX - boundaries.width / 2) / 25;

      functionalCard.style.transform = `rotateX(${inclinationX}deg) rotateY(${inclinationY}deg)`;
    });

    functionalCard.addEventListener("mouseleave", () => {
      functionalCard.style.transform = "rotateX(0deg) rotateY(0deg)";
    });
  }

  // 8. MATRIX BACKGROUND FLOATING PARTICLES ENGINE
  function constructParticle() {
    const spaceParticle = document.createElement("span");
    spaceParticle.className = "particle";
    spaceParticle.style.left = Math.random() * window.innerWidth + "px";

    // Random dimensions and speeds
    const diameter = Math.random() * 5 + 3 + "px";
    spaceParticle.style.width = diameter;
    spaceParticle.style.height = diameter;

    spaceParticle.style.animationDuration = Math.random() * 5 + 5 + "s";
    spaceParticle.style.opacity = Math.random() * 0.6 + 0.2;

    document.body.appendChild(spaceParticle);

    setTimeout(() => {
      spaceParticle.remove();
    }, 10000);
  }
  setInterval(constructParticle, 400);
});
