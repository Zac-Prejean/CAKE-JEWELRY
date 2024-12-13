// cubbysystem.js


const numberOfBoxes = 500; // Define the total number of boxes  
  
function reloadPage() {  
    setTimeout(() => {  
        location.reload();  
    }, 1000); // Wait for 1 second before reloading  
}  
setTimeout(reloadPage, 90000); // Reload every 90 seconds  
  
function createEmptyBoxes() {  
    const boxContainer = document.getElementById('boxContainer');  
    boxContainer.innerHTML = ''; // Clear previous boxes  
  
    for (let i = 1; i <= numberOfBoxes; i++) {  
        const box = document.createElement('div');  
        box.id = `box${i}`;  
        box.classList.add('emptybox');  
        boxContainer.appendChild(box);  
    }  
}  
  
function daysDifference(firstScannedTime) {  
    const currentTime = new Date();  
    const scannedDate = new Date(firstScannedTime);  
    const timeDifference = Math.abs(currentTime - scannedDate);  
    const daysDifference = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));  
    return daysDifference;  
}  
  
function displayCubbies(cubbies) {  
    createEmptyBoxes(); // Create the empty boxes first  

    // Group items by cubbyID  
    const cubbyGroups = cubbies.reduce((acc, cubby) => {  
        if (!acc[cubby.cubbyID]) {  
            acc[cubby.cubbyID] = [];  
        }  
        acc[cubby.cubbyID].push(cubby);  
        return acc;  
    }, {});  

    console.log('Cubby groups:', cubbyGroups);

    let boxesInUse = 0; // Initialize the count of boxes in use  

    // Populate the boxes with grouped items  
    for (const [cubbyID, cubbyItems] of Object.entries(cubbyGroups)) {  
        const box = document.getElementById(`box${cubbyID}`);  
        if (box) {  
            box.classList.remove('emptybox');  
            box.classList.add('box');  
            boxesInUse++; // Increment the count of boxes in use  

            let scannedOrders = {};  
            let colorBarStyle = '';  

            // Calculate total scanned quantities for each order  
            cubbyItems.forEach(item => {  
                const { orderID, qty } = item;  
                if (!scannedOrders[orderID]) {  
                    scannedOrders[orderID] = 0;  
                }  
                scannedOrders[orderID] += qty;  
            });  

            const { orderID, dateTime, total_qty } = cubbyItems[0];  
            const daysOld = daysDifference(dateTime);  
            const totalScannedQty = scannedOrders[orderID]; // Total scanned quantity for this order  

            // Store totalScannedQty and total_qty in the box element's dataset  
            box.dataset.totalScannedQty = totalScannedQty;  
            box.dataset.totalQty = total_qty;  

            // Calculate time difference in minutes  
            const firstScannedTime = new Date(cubbyItems[0].dateTime).getTime();  
            const currentTime = new Date().getTime();  
            const timeDifferenceMinutes = (currentTime - firstScannedTime) / 60000;  

            if (timeDifferenceMinutes <= 10) {  
                colorBarStyle = '#E65EA4'; // Set color-bar to #E65EA4 if within 10 minutes  
            } else if (totalScannedQty === parseInt(total_qty, 10)) {  
                colorBarStyle = '#44AF51';  
                // Change cancelCompleteBtn to confirmCompleteBtn  
                document.getElementById('cancelCompleteBtn').style.display = 'none';  
                document.getElementById('confirmCompleteBtn').style.display = 'inline-block';  
            } else if (daysOld > 1 && daysOld <= 2) {  
                colorBarStyle = '#F3A116';  
            } else if (daysOld > 2) {  
                colorBarStyle = '#D6324D';  
            }  

            const colorBar = document.createElement('div');  
            colorBar.className = 'color-bar';  
            colorBar.style.backgroundColor = colorBarStyle;  
            box.appendChild(colorBar);  

            const boxLabel = document.createElement('h4');  
            boxLabel.className = 'box-number box-number-overlay';  
            boxLabel.textContent = `${cubbyID}`;  
            box.appendChild(boxLabel);  

            const orderNumberLabel = document.createElement('p');  
            orderNumberLabel.textContent = `${orderID}`;  
            orderNumberLabel.style.fontSize = '13px'; // Set the font size to 13px  
            box.appendChild(orderNumberLabel);  

            // Display quantity in box / total_qty  
            const quantityLabel = document.createElement('p');  
            quantityLabel.textContent = `${totalScannedQty}/${total_qty}`;  
            box.appendChild(quantityLabel);  

            // Add event listener to trigger the modal  
            box.addEventListener('click', () => {  
                showBoxInfo(cubbyID, cubbyItems);  
            });  
        } else {  
            console.warn(`Box with cubbyID ${cubbyID} not found.`);  
        }  
    }  

    // Update the boxesInUse element with the count of used boxes  
    document.getElementById('boxesInUse').textContent = `${boxesInUse} BOXES IN USE`;  
}  
 
  
// Call the displayCubbies function when the page loads  
document.addEventListener('DOMContentLoaded', function() {  
    fetch('/get_cubbies')  
        .then(response => response.json())  
        .then(data => {  
            displayCubbies(data);  
        })  
        .catch(error => console.error('Error fetching cubby data:', error));  
});  
 
  
document.addEventListener('DOMContentLoaded', function () {  
    // Event listener for deleteBoxBtn  
    document.getElementById('deleteBoxBtn').addEventListener('click', function () {  
        const boxNumber = document.getElementById('boxInfoNumber').innerText;  
        const boxElement = document.getElementById(`box${boxNumber}`);  
  
        if (boxElement) {  
            const totalScannedQty = parseInt(boxElement.dataset.totalScannedQty, 10);  
            const totalQty = parseInt(boxElement.dataset.totalQty, 10);  
  
            if (totalScannedQty === totalQty) {  
                // Show the completeWarningModal if the items in the box equal the total_qty  
                document.getElementById('completeBoxNumber').innerText = boxNumber;  
                $('#completeWarningModal').modal('show');  
            } else {  
                // Show the deleteWarningModal if the items in the box do not equal the total_qty  
                document.getElementById('deleteBoxNumber').innerText = boxNumber;  
                $('#deleteWarningModal').modal('show');  
            }  
        }  
    });  
  
    // Event listener for cancelDeleteBtn inside deleteWarningModal  
    document.getElementById('cancelDeleteBtn').addEventListener('click', function () {  
        $('#deleteWarningModal').modal('hide');  
    });  
  
    // Event listener for confirmCompleteBtn  
    document.getElementById('confirmCompleteBtn').addEventListener('click', async function () {  
        const boxNumber = parseInt(document.getElementById('completeBoxNumber').innerText, 10);  
        completeBox(boxNumber);  
        $('#completeWarningModal').modal('hide');  
        $('#boxInfoModal').modal('hide');  
    });  
});  
  
function completeBox(boxNumber) {  
    // Implement the logic to handle completing the box  
    console.log(`Completing box ${boxNumber}`);  
}  
  
document.addEventListener('DOMContentLoaded', function() {  
    $('form.cubby-search-bar').on('submit', function(event) {  
        event.preventDefault();  
        const searchPattern = /^[a-zA-Z0-9]{8,20}$/;  
        const searchTerm = $('input[type="search"]').val().trim();  
        console.log(`Search term entered: ${searchTerm}`);  // Log the search term  

        if (!searchPattern.test(searchTerm)) {  
            $('#invalidNumberModal').modal('show');  
            $('input[type="search"]').val('');  
            return;  
        }  

        // Fetch the item details by itemID or orderID  
        $.get(`/search_item?search_term=${searchTerm}`, function(data) {  
            console.log('Search response:', data);  // Log the response from the server  
            if (data.error) {  
                $('#notScannedModal').modal('show');  
                $('input[type="search"]').val('');  
            } else {  
                // Assuming the first item in the data array is the item we want to show  
                const item = data[0];  
                const boxNumber = item.cubbyID;  
                showBoxInfo(boxNumber, data);  
                $('input[type="search"]').val('');  
            }  
        }).fail(function() {  
            $('#notScannedModal').modal('show');  
            $('input[type="search"]').val('');  
        });  
    });  
});   
  
function showBoxInfo(boxNumber, cubbyItems) {  
    // Set the modal content with the cubby details  
    document.getElementById('boxInfoNumber').innerText = boxNumber;  
  
    // Assuming all items in the cubby have the same order number and first scanned time  
    const { orderID, dateTime } = cubbyItems[0];  
    document.getElementById('boxInfoOrderNumber').innerHTML = `<a href="https://app.skulabs.com/order?store_id=66578a3a08851e1cf8e5cfcb&order_number=${orderID}" target="_blank" class="red-text" text-decoration: none;">${orderID}</a>`;  
    document.getElementById('boxInfoFirstScannedTime').innerText = dateTime;  
  
    const scannedItemsContainer = document.getElementById('scannedItems');  
    scannedItemsContainer.innerHTML = ''; // Clear previous items  
  
    let totalScannedQty = 0;  
    let totalQty = 0;  
  
    cubbyItems.forEach((item, index) => {  
        const itemElement = document.createElement('div');  
        itemElement.classList.add('item-details');  
        itemElement.innerHTML = `  
            <p><strong>Item ID:</strong> ${item.itemID}</p>  
            <p><strong>SKU:</strong> ${item.sku}</p>  
            <p><strong>Qty:</strong> ${item.qty}</p>  
        `;  
        scannedItemsContainer.appendChild(itemElement);  
  
        totalScannedQty += item.qty;  
        totalQty = item.total_qty; // Assuming total_qty is the same for all items in the cubby  
  
        // Add a horizontal line after each item except the last one  
        if (index < cubbyItems.length - 1) {  
            const hr = document.createElement('hr');  
            scannedItemsContainer.appendChild(hr);  
        }  
    });  
  
    // Check if totalScannedQty matches totalQty and update button visibility  
    if (totalScannedQty === parseInt(totalQty, 10)) {  
        document.getElementById('completeBoxBtn').style.display = 'inline-block';  
        document.getElementById('deleteBoxBtn').style.display = 'none';  
    } else {  
        document.getElementById('completeBoxBtn').style.display = 'none';  
        document.getElementById('deleteBoxBtn').style.display = 'inline-block';  
    }  
  
    // Show the modal  
    $('#boxInfoModal').modal('show');  
}   
  
// Call the displayCubbies function when the page loads  
document.addEventListener('DOMContentLoaded', function() {  
    fetch('/get_cubbies')  
        .then(response => response.json())  
        .then(data => {  
            displayCubbies(data);  
        })  
        .catch(error => console.error('Error fetching cubby data:', error));  
});  
  
// CLOSE BUTTON  
document.querySelectorAll('.closeModalBtn').forEach(function (closeBtn) {  
    closeBtn.addEventListener('click', function () {  
        if ($('#boxNumberModal').hasClass('show')) {  
            $('#boxNumberModal').modal('hide');  
        } else if ($('#boxInfoModal').hasClass('show')) {  
            $('#boxInfoModal').modal('hide');  
            $('input[type="search"]').focus();  
        } else if ($('#alreadyScannedModal').hasClass('show')) {  
            $('#alreadyScannedModal').modal('hide');  
        } else if ($('#notScannedModal').hasClass('show')) {  
            $('#notScannedModal').modal('hide');  
        } else if ($('#invalidNumberModal').hasClass('show')) {  
            $('#invalidNumberModal').modal('hide');  
        }  
    });  
});  
  
document.addEventListener('keydown', function (event) {  
    if (event.key === 'Enter' || event.key === 'Escape') {  
        if ($('#boxNumberModal').hasClass('show')) {  
            $('#boxNumberModal').modal('hide');  
        } else if ($('#boxInfoModal').hasClass('show')) {  
            $('#boxInfoModal').modal('hide');  
            $('input[type="search"]').focus();  
        } else if ($('#deleteWarningModal').hasClass('show')) {  
            $('#deleteWarningModal').modal('hide');  
            $('input[type="search"]').focus();  
        }  
    }  
});  

document.addEventListener('DOMContentLoaded', function() {  
    // Event listener for cancelDeleteBtn  
    document.getElementById('cancelDeleteBtn').addEventListener('click', function () {  
        $('#deleteWarningModal').modal('hide');  
        $('#boxInfoModal').modal('hide');  
        $('input[type="search"]').focus();  
    });  
  
    // Event listener for confirmCompleteBtn  
    document.getElementById('confirmCompleteBtn').addEventListener('click', async function () {  
        const boxNumber = parseInt(document.getElementById('completeBoxNumber').innerText, 10);  
        completeBox(boxNumber);  
        $('#completeWarningModal').modal('hide');  
        $('#boxInfoModal').modal('hide');  
  
        // Get the box items from the scanned items container  
        const scannedItemsContainer = document.getElementById('scannedItems');  
        const scannedItems = Array.from(scannedItemsContainer.children);  
  
        for (const itemElement of scannedItems) {  
            console.log("Scanned item textContent:", itemElement.textContent);  
        }  
  
        // Get unique order numbers in the box  
        const orderNumbers = new Set(scannedItems.map(itemElement => itemElement.textContent));  
        console.log("Order numbers:", Array.from(orderNumbers));  
    });  
  
    // Event listener for deleteBoxBtn  
    document.getElementById('deleteBoxBtn').addEventListener('click', function() {  
        const boxNumber = document.getElementById('boxInfoNumber').innerText;  
        document.getElementById('deleteBoxNumber').innerText = boxNumber;  
        $('#deleteWarningModal').modal('show');  
    });  
  
    // Event listener for cancelDeleteBtn inside deleteWarningModal  
    document.getElementById('cancelDeleteBtn').addEventListener('click', function() {  
        $('#deleteWarningModal').modal('hide');  
    });  
  
    // Event listener for confirmDeleteBtn  
    document.getElementById('confirmDeleteBtn').addEventListener('click', function() {  
        const password = document.getElementById('deletePasswordInput').value;  
        const boxNumber = document.getElementById('deleteBoxNumber').innerText;  
      
        // Send a request to the backend endpoint to check the password  
        fetch('/check_password', {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json',  
            },  
            body: JSON.stringify({ password: password }),  
        })  
        .then(response => response.json())  
        .then(data => {  
            if (data.result === 'success') {  
                // If the password is correct, proceed to delete the box  
                $.ajax({  
                    url: `/delete_cubby/${boxNumber}`,  
                    type: 'DELETE',  
                    success: function(result) {  
                        // Handle success  
                        console.log(result.message);  
                        $('#deleteWarningModal').modal('hide');  
                        $('#boxInfoModal').modal('hide');  
                        // Optionally reload the page or update the UI to reflect the deletion  
                        location.reload();  
                    },  
                    error: function(xhr, status, error) {  
                        // Handle error  
                        console.error(`Error deleting cubby: ${xhr.responseText}`);  
                        $('#deleteWarningModal').modal('hide');  
                        $('#boxInfoModal').modal('hide');  
                    }  
                });  
            } else {  
                // If the password is incorrect, show an alert  
                alert('Incorrect password. Please try again.');  
            }  
        })  
        .catch(error => {  
            console.error('Error checking password:', error);  
        });  
    });  
}); 

document.addEventListener('DOMContentLoaded', function() {  
    // Event listener for completeBoxBtn  
    document.getElementById('completeBoxBtn').addEventListener('click', function() {  
        const boxNumber = document.getElementById('boxInfoNumber').innerText;  
        document.getElementById('completeBoxNumber').innerText = boxNumber;  
        $('#completeWarningModal').modal('show');  
    });  
  
    // Event listener for confirmCompleteBtn  
    document.getElementById('confirmCompleteBtn').addEventListener('click', async function() {  
        const boxNumber = parseInt(document.getElementById('completeBoxNumber').innerText, 10);  
        completeBox(boxNumber);  
        $('#completeWarningModal').modal('hide');  
        $('#boxInfoModal').modal('hide');  
    });  
  
    // Event listener for cancelCompleteBtn  
    document.getElementById('cancelCompleteBtn').addEventListener('click', function() {  
        $('#completeWarningModal').modal('hide');  
    });  
});  
  
function completeBox(boxNumber) {  
    console.log(`Completing box ${boxNumber}`);  
    $.ajax({  
        url: `/delete_cubby/${boxNumber}`,  
        type: 'DELETE',  // Use DELETE method instead of POST for deletion  
        success: function(result) {  
            console.log(result.message);  
            location.reload();  
        },  
        error: function(xhr, status, error) {  
            console.error(`Error completing cubby: ${xhr.responseText}`);  
        }  
    });  
}