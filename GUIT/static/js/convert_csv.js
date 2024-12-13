// convert_csv.js

document.getElementById('download-button').addEventListener('click', async function () {  
    const fileInput = document.getElementById('csv-file');  
    if (fileInput.files.length > 0) {  
        const file = fileInput.files[0];  
        console.log("Selected file type: ", file.type);  
        if (file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||  
            file.type === "text/csv" ||  
            file.name.endsWith('.csv') ||  
            file.name.endsWith('.xlsx')) {  
            Papa.parse(file, {  
                header: true,  
                complete: async function (results) {  
                    const data = results.data;  
                    const convertedData = await convertCsvData(data);  
                    downloadCsv(convertedData);  
                }  
            });  
        } else {  
            alert("Invalid file type. Please upload a CSV or Excel file.");  
        }  
    } else {  
        alert("Please select a file to download.");  
    }  
}); 
  
async function getApiKey() {  
    const response = await fetch('/api/get-api-key');  
    const data = await response.json();  
    return data.api_key;  
}  
  
async function fetchMetadata(line_id, orderNumber) {  
    try {  
        const response = await fetch(`/api/fetch-metadata?line_id=${line_id}&orderNumber=${orderNumber}`);  
        if (response.ok) {  
            const data = await response.json();  
            return data.metadata;  
        } else {  
            console.error('Error fetching metadata:', response.statusText);  
            return null;  
        }  
    } catch (error) {  
        console.error('Error fetching metadata:', error);  
        return null;  
    }  
}  
  
async function fetchLocation(sku) {  
    const apiKey = await getApiKey();  
    try {  
        const response = await fetch(`/api/location?sku=${sku}`, {  
            headers: {  
                'Authorization': `Bearer ${apiKey}`  
            }  
        });  
        // Check if the response is JSON  
        const contentType = response.headers.get('content-type');  
        if (contentType && contentType.indexOf('application/json') !== -1) {  
            const data = await response.json();  
            return data.location || 'Location not found';  
        } else {  
            console.error('Response is not JSON:', response);  
            return 'Location not found';  
        }  
    } catch (error) {  
        console.error('Error fetching location:', error);  
        return 'Location not found';  
    }  
}  

function sleep(ms) {  
    return new Promise(resolve => setTimeout(resolve, ms));  
}

async function is3PLOrderWithRetry(orderNumber, retries = 3, delay = 3000) {  
    for (let attempt = 1; attempt <= retries; attempt++) {  
        try {    
            const response = await fetch('/api/sku-labs-batching', {  
                method: 'POST',  
                headers: { 'Content-Type': 'application/json' },  
                body: JSON.stringify({ orderNumber: orderNumber })  
            });  
            const result = await response.json();  
            return result.message === '3PL order' || result.message === 'not a completeful order skipping';  
        } catch (error) {  
            console.error(`Attempt ${attempt} - Error fetching order status for ${orderNumber}:`, error);  
            if (attempt < retries) {  
                await sleep(delay); // Wait before retrying  
            } else {  
                throw error; // Rethrow if all retries fail  
            }  
        }  
    }  
}        
  
async function processAndDownloadCsv(file) {  
    Papa.parse(file, {  
        header: true,  
        complete: async function (results) {  
            const convertedData = await convertCsvData(results.data);  
            downloadCsv(convertedData);  
        }  
    });  
}  
  
async function convertCsvData(data) {  
    const convertedData = [];  
    const fieldnames = ['Line - ID', 'Order - Number', 'Item - Qty', 'Total Order Qty', 'Item - SKU', 'Item - Options', 'Item - Name', 'Order - Date', 'Custom - Field 3'];  
    convertedData.push(fieldnames);  
  
    const monthMap = {  
        'January': 'JAN', 'February': 'FEB', 'March': 'MAR', 'April': 'APR',  
        'May': 'MAY', 'June': 'JUN', 'July': 'JUL', 'August': 'AUG',  
        'September': 'SEP', 'October': 'OCT', 'November': 'NOV', 'December': 'DEC'  
    };  
  
    let countQuantity = 0;  
    let countIndex = 1;  
  
    // Step 1: Calculate the total quantity for each order  
    const orderQuantities = {};  
    for (const row of data) {  
        const order_number = row['Order #'] ? row['Order #'].trim() : '';  
        const item_qty = row['Quantity'] ? parseInt(row['Quantity'].trim(), 10) : 0;  
        if (!order_number) continue;  
        if (!orderQuantities[order_number]) {  
            orderQuantities[order_number] = 0;  
        }  
        orderQuantities[order_number] += item_qty;  
    }  
  
    // Cache to store order status  
    const orderCache = {};  
  
    // Step 2: Process each row and include total order quantity in the item quantity  
    for (const row of data) {  
        const order_number = row['Order #'] ? row['Order #'].trim() : '';  
  
        // Check if the order is a 3PL order or not a completeful order and cache the result  
        if (order_number) {  
            if (!(order_number in orderCache)) {  
                try {  
                    orderCache[order_number] = await is3PLOrderWithRetry(order_number);  
                } catch (error) {  
                    console.error(`Failed to determine order status for ${order_number}. Skipping...`, error);  
                    continue;  
                }  
            }  
            if (orderCache[order_number]) {  
                console.log(`Order ${order_number} is a 3PL order. Skipping...`);  
                continue; // Skip not completeful orders and 3PL orders  
            } else {  
                console.log(`Order ${order_number} is not a 3PL order.`);  
            }  
        }  
  
        const line_id = row['Line ID'] ? row['Line ID'].trim() : '';  
        const item_qty = row['Quantity'] ? parseInt(row['Quantity'].trim(), 10) : 0;  
        const total_order_qty = orderQuantities[order_number];  
        let item_sku = row['3PL Partner SKU'] ? row['3PL Partner SKU'].trim() : '';  
        const line_name = row['Line Name'] ? row['Line Name'].trim() : '';  
        const order_date = formatOrderDate(row['Order Date'] ? row['Order Date'].trim() : '');  
        const design = row['personalization_1_value'] ? row['personalization_1_value'].trim() : '';  
        const personalization_1_key = row['personalization_1_key'] ? row['personalization_1_key'].trim() : '';  
        const personalization_1 = row['personalization_1_value'] ? row['personalization_1_value'].trim() : '';  
        const personalization_2 = row['personalization_2_value'] ? row['personalization_2_value'].trim() : '';  
        const personalization_3 = row['personalization_3_value'] ? row['personalization_3_value'].trim() : '';  
        const personalization_4 = row['personalization_4_value'] ? row['personalization_4_value'].trim() : '';  
        const personalization_5 = row['personalization_5_value'] ? row['personalization_5_value'].trim() : '';  
        const personalization_6 = row['personalization_6_value'] ? row['personalization_6_value'].trim() : '';  
        const personalization_7 = row['personalization_7_value'] ? row['personalization_7_value'].trim() : '';  
        
        let item_options = '';  
        if (item_sku === "") {  
            item_sku = row['SKU'] ? row['SKU'].trim() : '';  
        } 
        
                // // Extract personalizations dynamically  
                // let frontInscription = '';  
                // let rightInscription = '';  
                // let leftInscription = '';  
                // let backInscription = '';  
          
                // for (let i = 1; i <= 7; i++) {  
                //     const key = row[`personalization_${i}_key`] ? row[`personalization_${i}_key`].trim() : '';  
                //     const value = row[`personalization_${i}_value`] ? row[`personalization_${i}_value`].trim() : '';  
          
                //     if (key === 'Front Inscription') {  
                //         frontInscription = value;  
                //     } else if (key === 'Right Inscription') {  
                //         rightInscription = value;  
                //     } else if (key === 'Left Inscription') {  
                //         leftInscription = value;  
                //     } else if (key === 'Back Inscription') {  
                //         backInscription = value;  
                //     }  
                // } 
  
        // Process the row based on SKU and other criteria  
        const BirthNCK = ["NCKBFLGLDCHN01", "NCKBFLSILCHN01", "NCKBFLRSGCHN01"];  
        if (BirthNCK.includes(item_sku)) {  
            let monthAbbr = '';  
            for (const [month, abbr] of Object.entries(monthMap)) {  
                if (line_name.includes(month)) {  
                    monthAbbr = abbr;  
                    break;  
                }  
            }  
            item_sku = `NCK${monthAbbr}${item_sku}`;  
            item_options = `Design:Mon Amour Months, Personalization:${[personalization_4, personalization_5, personalization_6, personalization_7].filter(val => val).join('\n')}`;  
        } else if (item_sku.startsWith("NCKCLT")) {  
            const personalizations = [personalization_3];  
            item_options = `Design: Spaced Letter, Personalization:${personalizations}`;  
        } else if (item_sku.startsWith("NCK")) {  
            let personalizations;  
            if (personalization_1_key === "Left Inscription") {  
                personalizations = [personalization_1, personalization_2, personalization_3].filter(val => val).join('\n');  
            } else {  
                personalizations = personalization_4 ?  
                    [personalization_4, personalization_5, personalization_6, personalization_7].filter(val => val).join('\n') :  
                    personalization_2;  
            }  
            item_options = `Design:${design}, Personalization:${personalizations}`;  
        } else if (item_sku.startsWith("RNG")) {  
            const personalizations = [personalization_2, personalization_3].filter(val => val).join('\n');  
            item_options = `Personalization:${personalizations}`;  
        } else if (item_sku.startsWith("SRN")) {  
            const personalizations = [personalization_2];  
            item_options = `Design:${design}, Personalization:${personalizations}`;  
        } else if (item_sku.startsWith("BNCK")) {  
            let frontInscription = '';  
            let rightInscription = '';  
            let leftInscription = '';  
            let backInscription = '';  
          
            for (let i = 1; i <= 7; i++) {  
                const key = row[`personalization_${i}_key`] ? row[`personalization_${i}_key`].trim() : '';  
                const value = row[`personalization_${i}_value`] ? row[`personalization_${i}_value`].trim() : '';  
          
                if (key === 'Front Inscription') {  
                    frontInscription = value;  
                } else if (key === 'Right Inscription') {  
                    rightInscription = value;  
                } else if (key === 'Left Inscription') {  
                    leftInscription = value;  
                } else if (key === 'Back Inscription') {  
                    backInscription = value;  
                }  
            }  
          
            let inscriptions = [];  
            if (frontInscription) inscriptions.push(`Front Inscription: ${frontInscription}`);  
            if (rightInscription) inscriptions.push(`Right Inscription: ${rightInscription}`);  
            if (leftInscription) inscriptions.push(`Left Inscription: ${leftInscription}`);  
            if (backInscription) inscriptions.push(`Back Inscription: ${backInscription}`);  
            item_options = inscriptions.join(', '); 
        } else if (item_sku.startsWith("BCT")) {  
            const metadata = await fetchMetadata(line_id, order_number);  
            const outside_inscription = metadata ? metadata.outside_personalization || metadata.outside_personalization2 : '';  
            const inside_inscription = metadata ? metadata.inside_personalization || metadata.inside_personalization2 : '';  
            item_options = `Outside Inscription: ${outside_inscription}, Inside Inscription: ${inside_inscription}`;  
        } else if (item_sku.startsWith("RWTF") || item_sku.startsWith("DLTH")) {  
            item_options = `Outside Inscription: ${personalization_3}, Inside Inscription: ${personalization_4}`;
        } else {  
            const location = await fetchLocation(item_sku);  
            item_options = `Location: ${location}`;  
        }  
  
        const item_name = row['Name'] ? row['Name'].trim() : '';  
        let custom_field_3 = '';  
        const timestamp = new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' }).replace('/', '.');  
  
        if (item_sku.startsWith("NCKGLD") || item_sku.startsWith("NCK02GLD") || item_sku.startsWith("NCK03GLD") || item_sku.startsWith("NCK04GLD")) {  
            countQuantity += item_qty;  
            if (countQuantity + item_qty > 20) {  
                countIndex++;  
                countQuantity = 0;  
            }  
            custom_field_3 = `NCKGLD ${timestamp}.${countIndex}`;  
        } else if (item_sku.startsWith("NCKSIL") || item_sku.startsWith("NCK02SIL") || item_sku.startsWith("NCK03SIL") || item_sku.startsWith("NCK04SIL")) {  
            countQuantity += item_qty;  
            if (countQuantity + item_qty > 20) {  
                countIndex++;  
                countQuantity = 0;  
            }  
            custom_field_3 = `NCKSIL ${timestamp}.${countIndex}`;  
        } else if (item_sku.startsWith("NCKRSG") || item_sku.startsWith("NCK02RSG") || item_sku.startsWith("NCK03RSG") || item_sku.startsWith("NCK04RSG")) {  
            countQuantity += item_qty;  
            if (countQuantity + item_qty > 20) {  
                countIndex++;  
                countQuantity = 0;  
            }  
            custom_field_3 = `NCKRSG ${timestamp}.${countIndex}`;  
        } else if (item_sku.startsWith("RNG35GLD") || item_sku.startsWith("RNG46GLD") || item_sku.startsWith("RNG68GLD") || item_sku.startsWith("RNG78GLD") || item_sku.startsWith("RNG910GLD") || item_sku.startsWith("RNG911GLD")) {  
            countQuantity += item_qty;  
            if (countQuantity + item_qty > 20) {  
                countIndex++;  
                countQuantity = 0;  
            }  
            custom_field_3 = `RNGGDL ${timestamp}.${countIndex}`;  
        } else if (item_sku.startsWith("RNG35SIL") || item_sku.startsWith("RNG46SIL") || item_sku.startsWith("RNG68SIL") || item_sku.startsWith("RNG78SIL") || item_sku.startsWith("RNG910SIL") || item_sku.startsWith("RNG911SIL")) {  
            countQuantity += item_qty;  
            if (countQuantity + item_qty > 20) {  
                countIndex++;  
                countQuantity = 0;  
            }  
            custom_field_3 = `RNGSIL ${timestamp}.${countIndex}`;  
        } else if (item_sku.startsWith("RNG35RSG") || item_sku.startsWith("RNG46RSG") || item_sku.startsWith("RNG68RSG") || item_sku.startsWith("RNG78RSG") || item_sku.startsWith("RNG910RSG") || item_sku.startsWith("RNG911RSG")) {  
            countQuantity += item_qty;  
            if (countQuantity + item_qty > 20) {  
                countIndex++;  
                countQuantity = 0;  
            }  
            custom_field_3 = `RNGRSG ${timestamp}.${countIndex}`;  
        } else if (item_sku.startsWith("NCKCLT")) {  
            custom_field_3 = `NCKCLT ${timestamp}`;  
        } else if (item_sku.startsWith("SRN")) {  
            custom_field_3 = `SRN ${timestamp}`;  
        } else if (item_sku.startsWith("BCT") || item_sku.startsWith("BNCK") || item_sku.startsWith("RWTF") || item_sku.startsWith("DLTH")) {  
            custom_field_3 = `BCT ${timestamp}`;  
        } else if (item_sku) {  
            custom_field_3 = `PICK&PACK ${timestamp}`;  
        }  
  
        if (line_id || order_number || item_qty || item_sku || item_options || item_name || order_date) {  
            convertedData.push([line_id, order_number, item_qty, total_order_qty, item_sku, item_options, item_name, order_date, custom_field_3]);  
        }  
  
        console.log("Processed row:", {  
            line_id, order_number, item_qty, total_order_qty,  
            item_sku, item_options, item_name, order_date, custom_field_3  
        });  
    }  
  
    return convertedData;  
}   
   
function formatOrderDate(orderDate) {  
    if (!orderDate) return '';  
    const date = new Date(orderDate);  
    const month = date.getMonth() + 1; // Months are zero-indexed  
    const day = date.getDate();  
    const year = date.getFullYear();  
    return `${month}.${day}.${year}`;  
}  
  
function downloadCsv(data) {  
    const csvContent = Papa.unparse(data);  
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });  
    const url = URL.createObjectURL(blob);  
    const link = document.createElement("a");  
    link.setAttribute("href", url);  
    link.setAttribute("download", "converted_file.csv");  
    link.style.visibility = 'hidden';  
    document.body.appendChild(link);  
    link.click();  
    document.body.removeChild(link);  
}  
