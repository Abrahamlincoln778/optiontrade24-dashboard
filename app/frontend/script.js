// OptionTrade24 Dashboard Interactions

document.addEventListener("DOMContentLoaded", () => {
  animateProfit();
  const contactForm = document.getElementById("supportForm");

  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      showToast("Support request sent successfully!");
      setTimeout(() => {
        contactForm.reset();
      }, 1500);
    });
  }
});

function animateProfit() {
  const profitElement = document.getElementById("profitAmount");
  if (!profitElement) return;

  let current = 0;
  const target = parseFloat(profitElement.dataset.target);
  const increment = target / 100;

  const interval = setInterval(() => {
    current += increment;
    profitElement.textContent = "$" + current.toFixed(2);
    if (current >= target) {
      profitElement.textContent = "$" + target.toFixed(2);
      clearInterval(interval);
    }
  }, 20);
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
    toast.remove();
  }, 3000);
}