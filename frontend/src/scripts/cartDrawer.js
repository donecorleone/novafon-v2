/**
 * CartDrawer - Modal Dialog Management
 * 
 * Handles opening, closing, and basic interaction with the shopping cart drawer.
 * Provides modal dialog functionality with backdrop click-to-close behavior.
 * 
 * @author Novafon Development Team
 * @version 1.0.0
 */

document.addEventListener('DOMContentLoaded', () => {
  
  // Get DOM elements
  const openBtn = document.getElementById('open-drawer');
  const closeBtn = document.getElementById('close-drawer');
  const continueBtn = document.getElementById('continue-shopping');
  const drawer = document.getElementById('drawer');

  /**
   * Open the cart drawer modal
   * 
   * @function openDrawer
   * @returns {void}
   * @example
   * // Open the cart drawer
   * openDrawer();
   */
  function openDrawer() {
    drawer.showModal();
  }

  /**
   * Close the cart drawer modal
   * 
   * @function closeDrawer
   * @returns {void}
   * @example
   * // Close the cart drawer
   * closeDrawer();
   */
  function closeDrawer() {
    drawer.close();
  }

  // Open drawer button event listener
  openBtn?.addEventListener('click', openDrawer);

  // Close drawer button event listener
  closeBtn?.addEventListener('click', closeDrawer);

  // Continue shopping button event listener
  continueBtn?.addEventListener('click', closeDrawer);

  /**
   * Handle backdrop clicks to close drawer
   * 
   * Closes the drawer when clicking outside the dialog panel
   * but inside the dialog backdrop.
   * 
   * @param {Event} e - The click event
   */
  drawer?.addEventListener('click', (e) => {
    if (e.target === drawer) {
      closeDrawer();
    }
  });

});