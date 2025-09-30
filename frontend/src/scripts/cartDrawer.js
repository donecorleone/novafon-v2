// Einfacher CartDrawer - nur Grundfunktionen
document.addEventListener('DOMContentLoaded', () => {
  
  const openBtn = document.getElementById('open-drawer');
  const closeBtn = document.getElementById('close-drawer');
  const continueBtn = document.getElementById('continue-shopping');
  const drawer = document.getElementById('drawer');

  // Panel öffnen
  openBtn?.addEventListener('click', () => {
    drawer.showModal();
  });

  // Panel schließen
  closeBtn?.addEventListener('click', () => {
    drawer.close();
  });

  continueBtn?.addEventListener('click', () => {
    drawer.close();
  });

  // Klick außerhalb = Panel schließen
  drawer?.addEventListener('click', (e) => {
    if (e.target === drawer) {
      drawer.close();
    }
  });

});