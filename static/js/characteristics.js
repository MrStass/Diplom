document.getElementById('view-all-details').addEventListener('click', function() {
        var details = document.getElementById('all-details');
        var viewButtonContainer = document.getElementById('view-all-details-container');
        var hideButtonContainer = document.getElementById('hide-details-container');

        details.style.display = 'block';
        viewButtonContainer.style.display = 'none';
        hideButtonContainer.style.display = 'block';
    });

    document.getElementById('hide-all-details').addEventListener('click', function() {
        var details = document.getElementById('all-details');
        var viewButtonContainer = document.getElementById('view-all-details-container');
        var hideButtonContainer = document.getElementById('hide-details-container');

        details.style.display = 'none';
        viewButtonContainer.style.display = 'block';
        hideButtonContainer.style.display = 'none';
    });