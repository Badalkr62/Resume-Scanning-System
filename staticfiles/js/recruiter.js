// document.addEventListener("DOMContentLoaded", function () {
//   const menuBtn = document.querySelector(".menu-toggle");
//   const sidebar = document.getElementById("sidebar");

//   menuBtn.addEventListener("click", function () {
//     sidebar.classList.toggle("active");
//   });
// });
document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");

    if(menuBtn){

        menuBtn.addEventListener("click", function(){

            sidebar.classList.toggle("active");

        });

    }

});
