let imagePaths = {};  
let currentImage = 'front';  
  
async function getImagePath(scannedNumber, side) {  
    const imagePath = `/images/${scannedNumber}_${side}.png`;  
  
    try {  
        const response = await fetch(imagePath);  
        if (response.ok) {  
            return imagePath;  
        } else {  
            return null;  
        }  
    } catch (error) {  
        console.error('Error fetching image path:', error);  
        return null;  
    }  
}  
  
async function changestatus(scannedNumber) {  
    const [order_number, item_id] = scannedNumber.split("_");  
  
    // Add the filename to the request body  
    const filename = document.getElementById('txt-files-dropdown').value;  
  
    // Fetch the designed status using both filename and scannedNumber  
    const getStatusResponse = await fetch('/get_status', {  
        method: 'POST',  
        headers: {  
            'Content-Type': 'application/x-www-form-urlencoded',  
        },  
        body: `scanned_number=${scannedNumber}&filename=${filename}`,  
    });  
    const getStatusText = await getStatusResponse.text();  
  
    if (getStatusText.toUpperCase() === "CUBBY" || getStatusText.toUpperCase() === "SCANNED-OUT") {  
        showQuantityModal("Are you ready to ship?", "CONFIRM", "CANCEL", async function () {  
            await updateStatus(order_number, item_id, "Shipped", filename);  
        });  
    } else {  
        showModal(getStatusText);  
        return;  
    }  
  
    document.getElementsByName('scanned_number')[0].value = "";  
}  
  
async function updateStatus(order_number, item_id, new_status, filename) {  
    const updateStatusResponse = await fetch(`/update_all_items_status/${filename}`, {  
        method: 'POST',  
        headers: {  
            'Content-Type': 'application/x-www-form-urlencoded',  
        },  
        body: `order_number=${order_number}&new_status=Shipped`,  
    });  
    const updateStatusText = await updateStatusResponse.text();  
}  
  
function fetchDesignedStatus(fileName) {  
    fetch(`/get_designed_status/${fileName}`)

        .then(response => response.json())  
        .then(data => {  
            console.log('Designed status:', data);  
        })  
        .catch(error => {  
            console.error('Error fetching designed status:', error);  
        });  
}  
  
function showModal(status) {  
    const modal = document.getElementById("myModal");  
    const span = document.getElementsByClassName("close")[0];  
  
    document.getElementById("modal-text").innerHTML = `This item has processed the <a href="#" class="status-link">${status}</a> stage. Check with supervisor.`;  
    modal.style.display = "block";  
  
    span.onclick = function () {  
        modal.style.display = "none";  
    };  
  
    window.onclick = function (event) {  
        if (event.target == modal) {  
            modal.style.display = "none";  
        }  
    };  
}  

function showQuantityModal(message, confirmText, cancelText, onConfirm) {  
    const quantityModal = document.getElementById("quantityModal");  
    document.getElementById("modal-message").innerText = message;  
    document.getElementById("confirmButton").innerText = confirmText;  
    document.getElementById("cancelButton").innerText = cancelText;  
  
    document.getElementById("confirmButton").onclick = async function () {  
        await onConfirm();  
        quantityModal.style.display = "none";  
    };  
  
    document.getElementById("cancelButton").onclick = function () {  
        quantityModal.style.display = "none";  
    };  
  
    quantityModal.style.display = "block";  
} 