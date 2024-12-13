// tally.js

function reloadPage() { 
    setTimeout(() => {  
      location.reload();  
    }, 1000); // Wait for 1 second before reloading 
  }  
    
  setTimeout(reloadPage, 90000); // Reload every 90 seconds
  
document.addEventListener("DOMContentLoaded", function() {  
  const progressBars = document.querySelectorAll('.progress-container .progressbar');  

  progressBars.forEach(bar => {  
      const value = parseFloat(getComputedStyle(bar).getPropertyValue('--i'));  

      if (value > 50) {  
          bar.classList.add('high');  
          bar.classList.remove('low');  
      } else {  
          bar.classList.add('low');  
          bar.classList.remove('high');  
      }  
  });  
}); 
