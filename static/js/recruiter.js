document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.querySelector(".menu-toggle");
  const sidebar = document.getElementById("sidebar");

  menuBtn.addEventListener("click", function () {
    sidebar.classList.toggle("active");
  });
});
