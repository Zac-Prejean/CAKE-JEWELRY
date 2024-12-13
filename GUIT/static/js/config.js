

// NAVBAR
document.getElementById("productionBtn").addEventListener("click", toggleMegaBox);  
document.getElementById("productionBtnMobile").addEventListener("click", toggleMegaBox);  
  
function toggleMegaBox() {  
  var megaBox = document.querySelector(".mega-box");  
  megaBox.classList.toggle("active");  
}  
  
document.addEventListener("click", function(event) {  
  var megaBox = document.querySelector(".mega-box");  
  var productionBtn = document.getElementById("productionBtn");  
  var productionBtnMobile = document.getElementById("productionBtnMobile");  
  if (!megaBox.contains(event.target) && !productionBtn.contains(event.target) && !productionBtnMobile.contains(event.target)) {  
    megaBox.classList.remove("active");  
  }  
});