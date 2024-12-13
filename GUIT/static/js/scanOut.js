// scanOut.js

 

$(document).ready(function() {  
    function handleScanFormSubmit(event) {  
        event.preventDefault();  
        var scannedNumber = $(event.target).find('input[name="scanned_number"]').val();  
        console.log("Scanned Number:", scannedNumber);  
  
        if (!scannedNumber) {  
            // Clear the display fields if the scanned input is empty  
            clearDisplayFields();  
            return;  
        }  
  
        let dataToSend = {  
            signedInEmployeeName: signedInEmployeeName  
        };  
  
        if (scannedNumber.length === 14) {  
            dataToSend.line_id = scannedNumber;  
        } else {  
            dataToSend.custom_id = scannedNumber;  
        }  
  
        // Determine the station type based on the form ID  
        let station = 'scanOut';  
  
        $.ajax({  
            url: `/scan/${station}`,  
            type: 'POST',  
            contentType: 'application/json',  
            data: JSON.stringify(dataToSend),  
            success: function(response) {  
                if (response.sku) {  
                    $('#sku').text(response.sku);  
                    $('#qty').text(response.qty);  
                    $('#details').text(response.description);  
                    $('#item_id').text(response.line_id);  
                    $('#order_id').text(response.order_id);  
  
                    // Call the function to update the image if SKU starts with "RNG"  
                    updateImageBasedOnSKU(response.sku);  
                } else {  
                    // Clear the display fields if the response does not contain SKU  
                    clearDisplayFields();  
                }  
  
                if (response.total_qty > 1) {  
                    showQuantityModal(  
                        'Order has multiple items. Please write box number on label',  
                        'Confirm',  
                        response.line_id,  
                        response.sku,  
                        response.order_id,  
                        function() {  
                            console.log('Confirmed');  
                            // Handle the confirmation logic here  
                        },  
                        function() {  
                            console.log('Closed');  
                            // Handle the close logic here  
                        }  
                    );  
                } else {  
                    showSingleModal(  
                        'Confirm single item shipment',  
                        'Confirm',  
                        'Cancel',  
                        response.line_id,  
                        response.sku,  
                        response.order_id,  
                        function() {  
                            console.log('Confirmed');  
                        },  
                        function() {  
                            console.log('Closed');  
                        }  
                    );  
                }  
  
                // Clear the input field and set focus back to it  
                $(event.target).find('input[name="scanned_number"]').val('').focus();  
            },  
            error: function(xhr) {  
                var error = JSON.parse(xhr.responseText);  
                if (error.status) {  
                    document.getElementById("modal-text").innerHTML = `This item has processed the <a href="#" class="status-link">${error.status}</a> stage. Check with supervisor.`;  
                    $('#warningModal').modal({  
                        backdrop: 'static',  
                        keyboard: false  
                    }).modal('show');  
                } else {  
                    console.error('Error:', error);  
                }  
  
                // Clear the input field and set focus back to it  
                $(event.target).find('input[name="scanned_number"]').val('').focus();  
            }  
        });  
    }  
  
    function updateImageBasedOnSKU(sku) {  
        console.log("Updating image based on SKU:", sku);  
        var imgElement = $('#scanImage');  
        var imagePath = '';  
  
        if (sku.startsWith("NCKGLD") || sku.startsWith("NCKSIL") || sku.startsWith("NCKRSG")) {  
            imagePath = urls.nck1Image;  
        } else if (sku.startsWith('NCK02')) {  
            imagePath = urls.nck2Image;  
        } else if (sku.startsWith('NCK03')) {  
            imagePath = urls.nck3Image;  
        } else if (sku.startsWith('NCK04')) {  
            imagePath = urls.nck4Image;  
        } else if (sku.startsWith('RNG')) {  
            imagePath = urls.ringImage;  
        } else if (sku.startsWith('SRN')) {  
            imagePath = urls.srnImage;  
        } else if (sku.startsWith('BCT')) {  
            imagePath = urls.bctImage;  
        } else {  
            imagePath = urls.ppImage;  
        }  
  
        console.log("Setting image src to:", imagePath);  
        imgElement.attr('src', imagePath);  
        imgElement.show(); // Ensure the image is displayed  
    }  
  
    function clearDisplayFields() {  
        $('#sku').text('');  
        $('#qty').text('');  
        $('#details').text('');  
        $('#item_id').text('');  
        $('#order_id').text('');  
        $('#scanImage').hide();  
    }  
  
    // Disable submit button when a modal is shown  
    $('.modal').on('shown.bs.modal', function() {  
        disableSubmitButton();  
    });  
  
    // Enable submit button when a modal is hidden  
    $('.modal').on('hidden.bs.modal', function() {  
        enableSubmitButton();  
    });  
  
    // Function to disable the submit button  
    function disableSubmitButton() {  
        $(".search-btn").prop("disabled", true);  
    }  
  
    // Function to enable the submit button  
    function enableSubmitButton() {  
        $(".search-btn").prop("disabled", false);  
    }  
  
    $('#scanForm1').on('submit', handleScanFormSubmit);  
    $('#scanForm2').on('submit', handleScanFormSubmit);  
  
    $('#warningSubmitButton').on('click', function() {  
        var password = $('#warningPasswordInput').val();  
        var scannedNumber = $('input[name="scanned_number"]').val();  
  
        let dataToSend = {  
            signedInEmployeeName: signedInEmployeeName,  
            password: password  
        };  
  
        if (scannedNumber.length === 14) {  
            dataToSend.line_id = scannedNumber;  
        } else {  
            dataToSend.custom_id = scannedNumber;  
        }  
  
        $.ajax({  
            url: '/override_status',  
            type: 'POST',  
            contentType: 'application/json',  
            data: JSON.stringify(dataToSend),  
            success: function(response) {  
                $('#warningModal').modal('hide');  
                if (response.sku) {  
                    $('#sku').text(response.sku);  
                    $('#qty').text(response.qty);  
                    $('#details').text(response.description);  
                    $('#item_id').text(response.line_id);  
                    $('#order_id').text(response.order_id);  
  
                    // Call the function to update the image if SKU starts with "RNG"  
                    updateImageBasedOnSKU(response.sku);  
                } else {  
                    // Clear the display fields if the response does not contain SKU  
                    clearDisplayFields();  
                }  
  
                // Clear the input field and set focus back to it  
                $('input[name="scanned_number"]').val('').focus();  
            },  
            error: function(xhr) {  
                var error = JSON.parse(xhr.responseText);  
                console.error('Error:', error);  
  
                // Clear the input field and set focus back to it  
                $('input[name="scanned_number"]').val('').focus();  
            }  
        });  
    });  
  
    function showSingleModal(message, confirmText, cancelText, itemId, itemName, orderNumber, onConfirm, onClose) {  
        const modal = document.getElementById("singleModal");  
        const shipButton = document.getElementById("shipButton");  
        const cancelButton = document.getElementById("cancelButton");  
  
        if (!modal) {  
            console.error('Modal element not found');  
            return;  
        }  
  
        // Clear any previous content or event listeners  
        shipButton.innerText = confirmText;  
        cancelButton.innerText = cancelText;  
        shipButton.onclick = null;  
        cancelButton.onclick = null;  
        shipButton.style.display = "inline";  
        document.getElementById("modal-message").innerHTML = message;  
  
        if (cancelText) {  
            cancelButton.style.display = "inline";  
            cancelButton.innerText = cancelText;  
        } else {  
            cancelButton.style.display = "none";  
        }  
  
        // Use Bootstrap's modal method to show the modal with static backdrop and disabled keyboard  
        $(modal).modal({  
            backdrop: 'static',  
            keyboard: false  
        }).modal("show");  
  
        shipButton.onclick = async function() {  
            if (orderNumber) {  
                document.getElementById("modal-message").innerHTML = `Order Number: <a href="https://app.skulabs.com/order?store_id=66578a3a08851e1cf8e5cfcb&order_number=${orderNumber}" target="_blank">${orderNumber}</a>`;  
                shipButton.style.display = "none";  
  
                if (typeof onClose === 'function') {  
                    await onClose();  
                }  
            } else {  
                if (addedItems.includes(itemId)) {  
                    // Display a warning modal when the item is already added  
                    showModal("Cubby");  
                    return;  
                }  
                addedItems.push(itemId);  
                if (typeof onConfirm === 'function') {  
                    await onConfirm();  
                }  
                $(modal).modal("hide");  
            }  
        };  
  
        cancelButton.onclick = function() {  
            $(modal).modal("hide");  
        };  
  
        window.onclick = function(event) {  
            if (event.target == modal) {  
                $(modal).modal("hide");  
            }  
        };  
    }  
  
    let addedItems = [];  
    function showQuantityModal(message, confirmText, itemId, itemName, orderNumber, onConfirm, onClose) {  
        const modal = document.getElementById("quantityModal");  
        const shipButton = document.getElementById("quantity-shipButton");  
  
        if (!modal) {  
            console.error('Quantity Modal element not found');  
            return;  
        }  
  
        // Clear any previous content or event listeners  
        shipButton.innerText = confirmText;  
        shipButton.onclick = null;  
        shipButton.style.display = "inline";  
        document.getElementById("quantity-modal-message").innerHTML = message;  
  
        $(modal).modal({  
            backdrop: 'static',  
            keyboard: false  
        }).modal("show");  
  
        shipButton.onclick = async function() {  
            let dataToSend = {  
                signedInEmployeeName: signedInEmployeeName,  
                scanned_number: itemId  // Ensure scanned_number is included correctly  
            };  
  
            // Proceed with data transfer to cubby  
            if (!addedItems.includes(itemId)) {  
                addedItems.push(itemId);  
  
                console.log("Data to send:", dataToSend);  
  
                $.ajax({  
                    url: '/insert_to_cubby',  
                    type: 'POST',  
                    contentType: 'application/json',  
                    data: JSON.stringify(dataToSend),  
                    success: function(response) {  
                        if (typeof onConfirm === 'function') {  
                            onConfirm();  
                        }  
                        $(modal).modal("hide");  
  
                        // Use the cubbyID from the response to show the box number modal  
                        showBoxNumberModal(response.cubbyID);  
                    },  
                    error: function(xhr, status, error) {  
                        console.error('AJAX request failed:', xhr);  
                        console.error('Status:', status);  
                        console.error('Error:', error);  
                        var errorResponse = JSON.parse(xhr.responseText);  
                        console.error('Error Response:', errorResponse);  
                    }  
                });  
            } else {  
                showModal("Cubby");  
            }  
        };  
    }  
  
    function showBoxNumberModal(boxNumber) {  
        const boxNumberModal = document.getElementById("boxNumberModal");  
        document.getElementById("boxNumber").innerText = boxNumber;  
  
        // Add a CSS class to the modal window to trigger the transition  
        boxNumberModal.classList.add("show-modal");  
  
        // Show the modal window after a short delay to allow the transition to take effect  
        setTimeout(function() {  
            $(boxNumberModal).modal({  
                backdrop: 'static',  
                keyboard: false  
            }).modal("show");  
        }, 120);  
  
        const closeModalBtn = document.getElementsByClassName("closeModalBtn")[0];  
        closeModalBtn.onclick = function() {  
            $(boxNumberModal).modal("hide");  
        };  
    }  
});  
