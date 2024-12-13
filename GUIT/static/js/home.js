

function getImageSource(date) {  
    const month = date.getMonth() + 1;  
    const day = date.getDate();  
  
    // Modify the image sources based on your requirements  
    if (month === 1 && day === 4) {  
      return "/static/images/home/newyears.png";
    } else  if (month === 1 && day >= 5 && day <= 31) {  
        return "/static/images/home/winter.png";
    } else  if (month === 2 && day >= 1 && day <= 7) {  
        return "/static/images/home/winter.png";
    } else  if (month === 2 && day >= 8 && day <= 15) {  
        return "/static/images/home/valentine.png";
    } else  if (month === 2 && day >= 16 && day <= 29) {  
        return "/static/images/home/winter.png";
    } else  if (month === 3 && day >= 1 && day <= 9) {  
        return "/static/images/home/spring.png";
    } else  if (month === 3 && day >= 10 && day <= 19) {  
        return "/static/images/home/st.patrick's.png";
    } else  if (month === 3 && day >= 20 && day <= 30) {  
      return "/static/images/home/easter.png";
    } else if (month === 4 && day === 1) {   
        return "/static/images/home/aprilfools.png";
    } else if (month === 4 && day >= 2 && day <= 30) {   
        return "/static/images/home/spring.png";
    } else if (month === 5 && day >= 1 && day <= 8) {   
        return "/static/images/home/spring.png";
    } else if (month === 5 && day >= 9 && day <= 16) {   
        return "/static/images/home/mothersday.png";
    } else if (month === 5 && day >= 17 && day <= 23) {   
        return "/static/images/home/spring.png";
    } else if (month === 5 && day >= 24 && day <= 31) {   
        return "/static/images/home/memorialday.png";
    } else if (month === 6 && day >= 1 && day <= 30) {   
        return "/static/images/home/summer.png";
    } else if (month === 7 && day >= 1 && day <= 7) {   
        return "/static/images/home/independence.png";
    } else if (month === 7 && day >= 8 && day <= 31) {   
        return "/static/images/home/summer.png";
    } else if (month === 8 && day >= 1 && day <= 31) {   
        return "/static/images/home/summer.png";
    } else if (month === 9 && day >= 1 && day <= 30) {   
        return "/static/images/home/fall.png";
    } else if (month === 10 && day >= 1 && day <= 23) {   
        return "/static/images/home/fall.png";
    } else if (month === 10 && day >= 24 && day <= 31) {   
        return "/static/images/home/halloween.png";
    } else if (month === 11 && day >= 1 && day <= 20) {   
        return "/static/images/home/fall.png";
    } else if (month === 11 && day >= 21 && day <= 30) {   
        return "/static/images/home/thanksgiving.png";
    } else if (month === 12 && day >= 1 && day <= 15) {   
        return "/static/images/home/winter.png";
    } else if (month === 12 && day >= 16 && day <= 29) {   
        return "/static/images/home/christmas.png";
    } else if (month === 12 && day >= 30 && day <= 31) {   
        return "/static/images/home/newyears.png";
    } else {  
      return "/static/images/home/banner_reg.png";  
    }  
  }  
  
  function updateImageSource() {  
    const imageElement = document.getElementById("image");  
    const currentDate = new Date();  
    imageElement.src = getImageSource(currentDate);  
  }  
  
  // Call the function to update the image source based on the current date  
  document.addEventListener('DOMContentLoaded', function () {  
    updateImageSource();  
  }); 
