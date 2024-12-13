let originalTableContent;   
  
function reloadPage() {    
  location.reload();    
}    
    
setTimeout(reloadPage, 360000); // 6000 milliseconds = 1 minute  
   
function searchItemTag(searchValue) {  
    fetch(`/api/search?query=${encodeURIComponent(searchValue)}`)  
        .then(response => response.json())  
        .then(data => {  
            const tableBody = document.querySelector('#database-table tbody');  
            tableBody.innerHTML = '';  
  
            if (data.error) {  
                console.error(data.error);  
                tableBody.innerHTML = `<tr><td colspan="10">Error: ${data.error}</td></tr>`;  
                return;  
            }  
  
            if (data.length === 0) {  
                tableBody.innerHTML = `<tr><td colspan="10">No results found</td></tr>`;  
                return;  
            }  
  
            data.forEach(item => {  
                console.log('Status:', item.status); // Add this line to debug  
                const row = document.createElement('tr');  
                const statusForm = document.createElement('form');  
                statusForm.action = '/admin_update_status';  
                statusForm.method = 'POST';  
              
                const lineIdInput = document.createElement('input');  
                lineIdInput.type = 'hidden';  
                lineIdInput.name = 'line_id';  
                lineIdInput.value = item.line_id;  
              
                const orderIdInput = document.createElement('input');  
                orderIdInput.type = 'hidden';  
                orderIdInput.name = 'order_id';  
                orderIdInput.value = item.order_id;  
              
                const statusDropdown = document.createElement('select');  
                statusDropdown.name = 'status';  
                statusDropdown.innerHTML = `  
                    <option value="Batched" ${item.status === 'Batched' ? 'selected' : ''}>Batched</option>  
                    <option value="Scanned-In" ${item.status === 'Scanned-In' ? 'selected' : ''}>Scanned-In</option>  
                    <option value="Printed" ${item.status === 'Printed' ? 'selected' : ''}>Printed</option>  
                    <option value="Scanned-Out" ${item.status === 'Scanned-Out' ? 'selected' : ''}>Scanned-Out</option>  
                    <option value="Cubby" ${item.status === 'Cubby' ? 'selected' : ''}>Cubby</option>  
                    <option value="Shipped" ${item.status === 'Shipped' ? 'selected' : ''}>Shipped</option>  
                    <option value="ERROR" ${item.status === 'ERROR' ? 'selected' : ''}>ERROR</option>  
                `;  
              
                statusForm.appendChild(lineIdInput);  
                statusForm.appendChild(orderIdInput);  
                statusForm.appendChild(statusDropdown);  
              
                row.innerHTML = `  
                    <td>${item.line_id}</td>  
                    <td>${item.custom_id}</td>  
                    <td>${item.order_id}</td>  
                    <td class="sku-box">${item.sku}</td>  
                `;  
              
                const statusCell = document.createElement('td');  
                statusCell.appendChild(statusForm);  
                row.appendChild(statusCell);  
              
                row.innerHTML += `  
                    <td>${item.description}</td>  
                    <td>${item.datetime}</td>  
                    <td>${item.scannedby}</td>  
                    <td>${item.qty}</td>  
                    <td>${item.cubby}</td>  
                    <td>${item.order_date}</td>  
                `;  
              
                tableBody.appendChild(row);  
            });     
  
            // Attach event listener to delete buttons  
            document.querySelectorAll('.delete-button').forEach(button => {  
                button.addEventListener('click', function() {  
                    const lineId = this.getAttribute('data-line-id');  
                    const orderId = this.getAttribute('data-order-id');  
                    if (confirm('Are you sure you want to delete this item?')) {  
                        const formData = new FormData();  
                        formData.append('line_id', lineId);  
                        formData.append('order_id', orderId);  
  
                        fetch('/delete_item', {  
                            method: 'POST',  
                            body: formData  
                        })  
                        .then(response => response.json())  
                        .then(data => {  
                            if (data.error) {  
                                console.error('Error deleting item:', data.error);  
                            } else {  
                                console.log('Item deleted successfully');  
                                // Optionally, remove the row from the table  
                                this.closest('tr').remove();  
                            }  
                        })  
                        .catch(error => {  
                            console.error('Error deleting item:', error);  
                        });  
                    }  
                });  
            });  
  
            // Attach event listeners to status dropdowns for the search results  
            attachEventListenersToStatusDropdowns();  
        })  
        .catch(error => {  
            console.error('Error fetching search results:', error);  
            const tableBody = document.querySelector('#database-table tbody');  
            tableBody.innerHTML = `<tr><td colspan="10">Error: ${error.message}</td></tr>`;  
        });  
}  


function showPasswordModal() {  
    return new Promise((resolve, reject) => {  
      const passwordModal = new bootstrap.Modal(  
        document.getElementById("passwordModal")  
      );  
      const submitButton = document.querySelector("#passwordModal .btn-primary");  
      const passwordInput = document.querySelector("#passwordModal #passwordInput");  
  
      passwordModal.show();  
  
      function handleModalHidden(event) {  
        submitButton.removeEventListener("click", handleSubmitButtonClick);  
        passwordInput.removeEventListener("keydown", handlePasswordInputKeydown);  
      }  
  
      function handleSubmitButtonClick() {  
        const password = passwordInput.value;  
  
        checkPassword(password)  
          .then(() => {  
            passwordInput.value = "";  
            passwordModal.hide();  
            resolve(password);  
          })  
          .catch(() => {  
            passwordInput.value = "";  
            reject();  
          });  
      }  
  
      function handlePasswordInputKeydown(event) {  
        if (event.key === "Enter") {  
          submitButton.click();  
        }  
      }  
  
      document.getElementById("passwordModal").addEventListener("hidden.bs.modal", handleModalHidden, { once: true });  
      submitButton.addEventListener("click", handleSubmitButtonClick);  
      passwordInput.addEventListener("keydown", handlePasswordInputKeydown);  
    });  
  }  

function checkPassword(input_password) {      
  return new Promise((resolve, reject) => { 
    fetch('/check_password', {  
      method: 'POST',  
      body: JSON.stringify({ password: input_password }),  
      headers: {  
        'Content-Type': 'application/json'  
      }  
    })  
    .then(response => {  
      if (!response.ok) {  
        throw new Error('Network response was not ok');  
      }  
      return response.json();  
    })  
    .then(data => {
  
      if (data.result !== 'failure') {  
        resolve();  
      } else {  
        alert('Incorrect password. Access denied.');  
        reject();  
      }  
    })  
    .catch(error => {  
      console.error('There was a problem with the fetch operation:', error);  
      reject();  
    });  
  });  
}   

function confirmDeleteBox() {  
  const password = document.getElementById('deletePasswordInput').value;  

  // Send a request to the Flask endpoint to check the password  
  fetch('/check_password', {  
      method: 'POST',  
      headers: {  
          'Content-Type': 'application/json',  
      },  
      body: JSON.stringify({password: password}),  
  })  
  .then(response => response.json())  
  .then(data => {  
      if (data.result === 'success') {  
          const boxNumber = parseInt(document.getElementById('deleteBoxNumber').innerText, 10);  
          removeBox(boxNumber);  

          // Clear the password input field  
          document.getElementById('deletePasswordInput').value = '';  

          // Close the delete warning modal  
          $('#deleteWarningModal').modal('hide');  
          // Close the box info modal  
          $('#boxInfoModal').modal('hide');  
      } else {  
          alert('Incorrect password. Please try again.');  
      }  
  });  
}

function getBackgroundColor(status) {  
  switch (status) {  
      case 'Batched':  
          return '#736B99';  
      case 'Scanned-In':  
          return '#9094CC';  
      case 'Printed':  
          return '#ABBDFF';  
      case 'Scanned-Out':  
          return '#B38EDE';  
      case 'Cubby':  
          return '#BF5F97';  
      case 'Shipped':  
          return '#CC5566';  
        case 'ERROR':  
          return '#D6324D'; 
      default:  
          return '';  
  }  
}  

// document.addEventListener('DOMContentLoaded', function() {  
//   // Check if you are on the admin page  
//   if (document.getElementById('admin-page')) {  
//       showPasswordModal()  
//           .then(password => {  
//               return checkPassword(password);  
//           })  
//           .then(() => {  
//               // The password is correct, display the content container and initialize your admin page here  
//               document.querySelector('.content-container').style.display = 'block';  
                
//               // Attach event listener to status dropdowns  
//               document.querySelectorAll('select[name="status"]').forEach(select => {  
//                   const updateDropdownBackgroundColor = () => {  
//                       const selectedOption = select.options[select.selectedIndex];  
//                       select.style.backgroundColor = getBackgroundColor(selectedOption.value);  
//                   };  

//                   // Initial background color setting  
//                   updateDropdownBackgroundColor();  

//                   select.addEventListener('change', function() {  
//                       const form = this.closest('form');  
//                       const formData = new FormData(form);  
//                       fetch(form.action, {  
//                           method: 'POST',  
//                           body: formData  
//                       })  
//                       .then(response => response.json())  
//                       .then(data => {  
//                           if (data.error) {  
//                               console.error('Error updating status:', data.error);  
//                           } else {  
//                               console.log('Status updated successfully');  
//                               // Optionally, update the UI to reflect the new status  
//                           }  
//                       })  
//                       .catch(error => {  
//                           console.error('Error updating status:', error);
                            
//                       });  
//                       updateDropdownBackgroundColor();  
//                   });  
//               });  
//           })  
//           .catch(() => {  
//               // The password is incorrect or not entered, the user is redirected to the home route  
//               window.location.href = '/';  
//           });  
//   }  

document.addEventListener('DOMContentLoaded', function() {  
    // Check if you are on the admin page  
    if (document.getElementById('admin-page')) {  
        showPasswordModal()  
            .then(password => {  
                return checkPassword(password);  
            })  
            .then(() => {  
                // The password is correct, display the content container and initialize your admin page here  
                document.querySelector('.content-container').style.display = 'block';  
                // Attach event listeners to status dropdowns  
                attachEventListenersToStatusDropdowns();  
            })  
            .catch(() => {  
                // The password is incorrect or not entered, the user is redirected to the home route  
                window.location.href = '/';  
            });  
    }  
}); 

  var deleteBoxBtn = document.getElementById('deleteBoxBtn');  
  if (deleteBoxBtn) {  
      deleteBoxBtn.addEventListener('click', function () {  
          const boxNumber = parseInt(document.getElementById('boxInfoNumber').innerText, 10);  
          deleteBox(boxNumber);  
      });  
  }  
  var confirmDeleteBtn = document.getElementById('confirmDeleteBtn');  
  if (confirmDeleteBtn) {  
      confirmDeleteBtn.addEventListener('click', confirmDeleteBox);  
  }  
  // Add event listeners for the password modal  
  if (document.getElementById('passwordModal')) {  
      document.getElementById('passwordModal').addEventListener('shown.bs.modal', function () {  
          document.getElementById('passwordInput').focus();  
      });  

      document.getElementById('passwordModal').addEventListener('hidden.bs.modal', function () {  
          document.getElementById('passwordInput').value = '';  
      });  
  }  

 

document.addEventListener('DOMContentLoaded', function() {  
  // Check if the main element exists  
  const mainElement = document.querySelector('main');  
  if (mainElement) {  
      showPasswordModal()  
          .then(password => {  
              return checkPassword(password);  
          })  
          .then(() => {  
              // The password is correct, display the main element  
              mainElement.style.display = 'block';  
          })  
          .catch(() => {  
              // The password is incorrect or not entered, the user is redirected to the home route  
              window.location.href = '/';  
          });  
  }  
});  

function showWarningModal() {  
  return new Promise((resolve, reject) => {  
      const warningModal = new bootstrap.Modal(document.getElementById("warningModal"));  
      const submitButton = document.querySelector("#warningModal .btn-primary");  

      warningModal.show();  

      function handleModalHidden(event) {  
          submitButton.removeEventListener("click", handleSubmitButtonClick);  
      }  

      function handleSubmitButtonClick() {  
          const passwordInput = document.querySelector("#warningModal #warningPasswordInput");  
          const password = passwordInput.value;  
          checkPassword(password)  
              .then(() => {  
                  passwordInput.value = "";  
                  warningModal.hide();  
                  resolve(password);  
              })  
              .catch(() => {  
                  passwordInput.value = "";  
                  reject();  
              });  
      }  

      document.getElementById("warningModal").addEventListener("hidden.bs.modal", handleModalHidden, { once: true });  
      submitButton.addEventListener("click", handleSubmitButtonClick);  
  });  
}  

function showModal(status) {  
  const modal = document.getElementById("warningModal");  
  const mainElement = document.querySelector('main');  

  document.getElementById("modal-text").innerHTML = `This item has processed the <a href="#" class="status-link">${status}</a> stage. Check with supervisor.`;  

  // Hide main element when showing the warning modal  
  mainElement.style.display = 'none';  

  showWarningModal()  
      .then(() => {  
          // Password was correct, proceed with further actions  
          mainElement.style.display = 'block';  
          modal.style.display = "none";  
      })  
      .catch(() => {  
          // Password was incorrect  
          alert("Incorrect password. Access denied.");  
      });  
}  

document.addEventListener('DOMContentLoaded', function() {  
  const mainElement = document.querySelector('main');  
    
  if (mainElement) {  
      showPasswordModal()  
          .then(password => {  
              return checkPassword(password);  
          })  
          .then(() => {  
              // The password is correct, display the main element  
              mainElement.style.display = 'block';  
          })  
          .catch(() => {  
              // The password is incorrect or not entered, the user is redirected to the home route  
              window.location.href = '/';  
          });  
  }  
});   

document.addEventListener('DOMContentLoaded', function() {  

    // Attach event listener to delete buttons  
    document.querySelectorAll('.delete-button').forEach(button => {  
        button.addEventListener('click', function() {  
            const lineId = this.getAttribute('data-line-id');  
            const orderId = this.getAttribute('data-order-id');  
            if (confirm('Are you sure you want to delete this item?')) {  
                const formData = new FormData();  
                formData.append('line_id', lineId);  
                formData.append('order_id', orderId);  
  
                fetch('/delete_item', {  
                    method: 'POST',  
                    body: formData  
                })  
                .then(response => response.json())  
                .then(data => {  
                    if (data.error) {  
                        console.error('Error deleting item:', data.error);  
                    } else {  
                        console.log('Item deleted successfully');  
                        // Optionally, remove the row from the table  
                        this.closest('tr').remove();  
                    }  
                })  
                .catch(error => {  
                    console.error('Error deleting item:', error);  
                });  
            }  
        });  
    });  
});  

function attachEventListenersToStatusDropdowns() {  
    document.querySelectorAll('select[name="status"]').forEach(select => {  
        const updateDropdownBackgroundColor = () => {  
            const selectedOption = select.options[select.selectedIndex];  
            select.style.backgroundColor = getBackgroundColor(selectedOption.value);  
        };  
  
        // Initial background color setting  
        updateDropdownBackgroundColor();  
  
        select.addEventListener('change', function() {  
            const form = this.closest('form');  
            const formData = new FormData(form);  
            fetch(form.action, {  
                method: 'POST',  
                body: formData  
            })  
            .then(response => response.json())  
            .then(data => {  
                if (data.error) {  
                    console.error('Error updating status:', data.error);  
                } else {  
                    console.log('Status updated successfully');  
                    // Optionally, update the UI to reflect the new status  
                }  
            })  
            .catch(error => {  
                console.error('Error updating status:', error);  
            });  
            updateDropdownBackgroundColor();  
        });  
    });  
}  

function filterByDate() {  
    const startDate = document.getElementById('startDate').value;  
    const endDate = document.getElementById('endDate').value;  
  
    const tableRows = document.querySelectorAll('#database-table tbody tr');  
  
    tableRows.forEach(row => {  
        const orderDate = row.querySelector('td:nth-child(10)').innerText; // Adjust the index if needed  
        const orderDateObj = new Date(orderDate);  
  
        if ((startDate && orderDateObj < new Date(startDate)) || (endDate && orderDateObj > new Date(endDate))) {  
            row.style.display = 'none';  
        } else {  
            row.style.display = '';  
        }  
    });  
}  
