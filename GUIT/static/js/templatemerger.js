
// Array to store the loaded PNGs
const loadedPNGs = [];

const fileInput = document.getElementById('file-input');
const previewArea = document.getElementById('preview-area');
const exportButton = document.getElementById('export-button');

// Add event listeners to the file input and export button
fileInput.addEventListener('change', handleFileInputChange);
exportButton.addEventListener('click', handleExportButtonClick);



// Function to change through formats
document.querySelector("#rings").addEventListener("click", function () {
  const dropdown = document.querySelector("#format-btn");
  dropdown.innerText = "Rings";
});

document.querySelector("#necklace").addEventListener("click", function () {
  const dropdown = document.querySelector("#format-btn");
  dropdown.innerText = "Necklace";
});

// document.querySelector("#one-name-necklace").addEventListener("click", function () {
//   const dropdown = document.querySelector("#format-btn");
//   dropdown.innerText = "One Name Necklace";
// });

// document.querySelector("#two-name-necklace").addEventListener("click", function () {
//   const dropdown = document.querySelector("#format-btn");
//   dropdown.innerText = "Two Name Necklace";
// });

// document.querySelector("#three-name-necklace").addEventListener("click", function () {
//   const dropdown = document.querySelector("#format-btn");
//   dropdown.innerText = "Three Name Necklace";
// });

// document.querySelector("#four-name-necklace").addEventListener("click", function () {
//   const dropdown = document.querySelector("#format-btn");
//   dropdown.innerText = "Four Name Necklace";
// });

// Handle file input change event
function handleFileInputChange(event) {
  previewArea.innerHTML = '';
  loadedPNGs.length = 0;
  const files = event.target.files;
  let counter = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];

    const reader = new FileReader();

    reader.onload = function (e) {
      const img = new Image();

      img.onload = function () {
        loadedPNGs.push(img);
        counter++;
        if (counter === files.length) {
          generatePreview();
        }
      };

      img.src = e.target.result;
      previewArea.appendChild(img);
    };
    reader.readAsDataURL(file);
  }
}

function handleExportButtonClick() {

  
  // JEWELRY
  function generateJewelryCanvas(numFilesLimit, fileName) {
    const files = document.getElementById('file-input').files;
    if (files.length > numFilesLimit) {
      alert(`Error: You can only select up to ${numFilesLimit} images.`);
      return;
    }
    generatePreview();
    setTimeout(() => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      const canvasWidthInches = 24;
      const dpi72 = 72.01558002 * 5;
      const canvasWidth = canvasWidthInches * dpi72;

      const numRows = Math.ceil(loadedPNGs.length / 2);

      const paddingY = 100;
      const canvasHeight = numRows * (loadedPNGs[0].height + paddingY) + paddingY;
      canvas.width = canvasWidth;
      canvas.height = canvasHeight;

      for (let i = 0; i < loadedPNGs.length; i++) {
        const loadedPNG = loadedPNGs[i];
        const col = i % 2;
        const row = Math.floor(i / 2);
        const x = col * (canvasWidth / 2);
        const y = row * (loadedPNG.height + paddingY) + paddingY;
        ctx.drawImage(loadedPNG, x, y, loadedPNG.width, loadedPNG.height);
      }
      const dataURL = canvas.toDataURL('image/png', 1);
      const blob = dataURLToBlob(dataURL);

      // Create a download link for the Blob  
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = fileName;
      link.click();
    }, 100);
  }

  // RINGS

  if (document.querySelector("#format-btn").innerText === "Rings") {
    generateJewelryCanvas(50, 'rings.png');
  }
  // NCK

    else if (document.querySelector("#format-btn").innerText === "Necklace") {
    generateJewelryCanvas(50, 'NCK.png');
  }

  // // NCK01 

  // else if (document.querySelector("#format-btn").innerText === "One Name Necklace") {
  //   generateJewelryCanvas(50, 'NCK01.png');
  // }

  // // NCK02 

  // else if (document.querySelector("#format-btn").innerText === "Two Name Necklace") {
  //   generateJewelryCanvas(35, 'NCK02.png');
  // }

  // // NCK03  

  // else if (document.querySelector("#format-btn").innerText === "Three Name Necklace") {
  //   generateJewelryCanvas(20, 'NCK03.png');
  // }

  // // NCK04 

  // else if (document.querySelector("#format-btn").innerText === "Four Name Necklace") {
  //   generateJewelryCanvas(20, 'NCK04.png');
// }

}

// Function to generate and display the preview of the final image
function generatePreview() {

  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  const exportButton = document.getElementById('export-button');
  exportButton.addEventListener('click', handleExportButtonClick);

  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';

  const canvasWidth = 800;
  const canvasHeight = 1200;
  canvas.width = canvasWidth;
  canvas.height = canvasHeight;

  const scaleFactor = Math.min(canvasWidth / 2400, canvasHeight / (loadedPNGs.length * 200));

  for (let i = 0; i < loadedPNGs.length; i++) {
    const loadedPNG = loadedPNGs[i];

    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 20 + col * (400 + 20);
    const y = 20 + row * (200 * scaleFactor + 20);

    ctx.drawImage(loadedPNG, x, y, 400 * scaleFactor, 200 * scaleFactor);
  }

  // Convert the canvas to a data URL
  const dataURL = canvas.toDataURL('image/png');

  // Create an <img> element for previewing the final image
  const previewImage = document.createElement('img');
  previewImage.src = dataURL;
  previewImage.classList.add('preview-pdf');

  // Clear the preview area and append the preview image
  previewArea.innerHTML = '';
  previewArea.appendChild(previewImage);
}

// Function to convert data URL to Blob
function dataURLToBlob(dataURL) {
  const binaryString = atob(dataURL.split(',')[1]);
  const arrayBuffer = new ArrayBuffer(binaryString.length);
  const view = new Uint8Array(arrayBuffer);
  for (let i = 0; i < binaryString.length; i++) {
    view[i] = binaryString.charCodeAt(i);
  }
  const blob = new Blob([arrayBuffer], { type: 'image/png' });

  return blob;
}  
