// scanin.js



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
        let station = 'scanIn';  
  
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
  
                // Clear the input field and set focus back to it  
                $(event.target).find('input[name="scanned_number"]').val('').focus();  
            },  
            error: function(xhr) {  
                var error = JSON.parse(xhr.responseText);  
                if (error.status) {  
                    document.getElementById("modal-text").innerHTML = `This item was last processed in the <a href="#" class="status-link">${error.status}</a> stage. Check with supervisor.`;  
                    $('#warningModal').modal('show');  
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
            },  
            error: function(xhr) {  
                var error = JSON.parse(xhr.responseText);  
                console.error('Error:', error);  
            }  
        });  
    });  
});  
