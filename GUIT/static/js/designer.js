// designer.js

document.addEventListener('DOMContentLoaded', function () {  
    const form = document.querySelector('form');  
    const terminalOutput = document.getElementById('terminalOutput');  
    const folderOrganizationCheckbox = document.getElementById('folderOrganizationCheckbox');  
  
    form.addEventListener('submit', async function (event) {  
        event.preventDefault();  
  
        const formData = new FormData(form);  
        formData.append('folderOrganization', folderOrganizationCheckbox.checked);  
  
        terminalOutput.innerHTML = '';  
  
        // Show the "Starting download..." message  
        terminalOutput.innerHTML = '<p>Starting download...</p>';  
  
        try {  
            const response = await fetch('/run-script', { method: 'POST', body: formData });  
  
            // Clear the "Starting download..." message  
            terminalOutput.innerHTML = '';  
  
            const reader = response.body.getReader();  
            const decoder = new TextDecoder('utf-8');  
  
            while (true) {  
                const { value, done } = await reader.read();  
                if (done) break;  
  
                const decodedValue = decoder.decode(value);  
                terminalOutput.innerHTML += decodedValue;  
                terminalOutput.scrollTop = terminalOutput.scrollHeight;  
            }  
        } catch (error) {  
            console.error('Error:', error);  
            terminalOutput.innerHTML = 'An error occurred while processing the CSV file. Please try again.';  
        }  
    });  
});  
