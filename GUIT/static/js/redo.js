// redo.js

let matchedImages = [];  
let currentIndex = 0;  
let order = [];  
  
document.getElementById('redoForm').addEventListener('submit', function(event) {  
    event.preventDefault();  
});  
  
document.getElementById('redobutton').addEventListener('click', function() {  
    const barcode = document.getElementById('barcode').value;  
    const itemBarcode = document.getElementById('itemBarcode').value;  
    const reason = document.getElementById('reason_string').value;  
    const user = document.getElementById('signedInUser').innerText;  
  
    if (barcode && itemBarcode && reason) {  
        submit_redo(barcode, itemBarcode, reason, user);  
        updateStatus(itemBarcode, 'ERROR');  
        document.getElementById('barcode').value = '';  
        document.getElementById('itemBarcode').value = '';  
        document.getElementById('reason_string').selectedIndex = 0;  
        document.getElementById('barcode').focus();  
    } else {  
        showMessage('Please fill out all fields.', 'red');  
    }  
});  
  
async function submit_redo(barcode, itemBarcode, reason, user) {  
    try {  
        const response = await fetch('/submit_redo', {  
            method: 'POST',  
            headers: { 'Content-Type': 'application/json' },  
            body: JSON.stringify({ "barcode": barcode, "itemBarcode": itemBarcode, "reason": reason, "user": user })  
        });  
        const result = await response.json();  
        if (result.status === 'success') {  
            showMessage(result.message, 'green');  
        } else {  
            showMessage(result.message, 'red');  
        }  
    } catch (error) {  
        showMessage('An error occurred: ' + error, 'red');  
    }  
}  
  
function showMessage(message, color) {  
    const messageElement = document.getElementById('message');  
    messageElement.textContent = message;  
    messageElement.style.color = color;  
}  
  
async function updateStatus(line_id, new_status) {  
    try {  
        console.log("Updating status for line_id:", line_id, "with new_status:", new_status);
        const response = await fetch('/update_status', {  
            method: 'POST',  
            headers: { 'Content-Type': 'application/json' },  
            body: JSON.stringify({ "line_id": line_id, "new_status": new_status })  
        });  
        const result = await response.json();  
        console.log("Response from server:", result); 
        if (result.message) {  
            showMessage(result.message, 'green');  
        } else {  
            showMessage(result.error, 'red');  
        }  
    } catch (error) {  
        console.log("Error occurred while updating status:", error);
        showMessage('An error occurred: ' + error, 'red');  
    }  
}  