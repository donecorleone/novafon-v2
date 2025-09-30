/**
 * Customer ID Management
 * 
 * Handles customer ID input and stores it globally for all components.
 * 
 */

// Get customer ID from user input and store globally
let customerId = prompt("Customer ID (C1001 oder C1002, Enter für C1001):");
if (!customerId || customerId.trim() === "") {
  customerId = "C1001";
}
// Store globally so all components can use it
window.customerId = customerId;

// Clear cart on reload to avoid mixing items between customers
fetch('http://localhost:8000/cart', { 
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ items: [] })
})
  .catch(err => console.log('Cart clear failed:', err));
