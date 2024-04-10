document.addEventListener('DOMContentLoaded', function() {
  var popupOverlay = document.querySelector('.popup-overlay');
  var popup = document.querySelector('.popup');
  var closeButton = document.getElementById('close-popup');

  // Function to show the popup
  function showPopup() {
    popupOverlay.style.display = 'block';
    popup.style.display = 'block';
  }

  // Function to hide the popup
  function hidePopup() {
    popupOverlay.style.display = 'none';
    popup.style.display = 'none';
  }

  // Event listener for close button click
  closeButton.addEventListener('click', function() {
    hidePopup();
  });

  // Event listener to show the popup
  // (You can call this function whenever you want to show the popup)
  showPopup();
});
