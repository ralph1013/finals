document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
  
    // Example using FullCalendar
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: '/get-appointments/',
      dateClick: function (info) {
  
        dateInput.value = info.dateStr; 
      },
      selectable: true, 
    });
  
    calendar.render();


    timeInput.addEventListener('click', function () {
    
      alert('Time picker integration goes here!');
    });
  });

function showSection(sectionId) {
  document.querySelectorAll('.section').forEach(section => {
    section.style.display = 'none';
  });
  document.getElementById(sectionId).style.display = 'block';
}

function showPostDetail(postId) {
  fetch(`/${postId}/`)
    .then(response => response.json())
    .then(data => {
      document.getElementById('detail-title').textContent = data.post.title;
      document.getElementById('detail-body').textContent = data.post.body;
      document.getElementById('edit-button').onclick = () => showEditForm(postId);
      document.getElementById('delete-button').onclick = () => showDeleteConfirmation(postId);
      showSection('post-detail');
    });
}

function showEditForm(postId) {
  document.getElementById('edit-form').action = `/blogs/${postId}/`;
  showSection('edit-post');
}

function showDeleteConfirmation(postId) {
  const deleteForm = document.querySelector('#delete-form');
  deleteForm.action = `/blogs/${postId}/`; // Set the correct endpoint for deletion
  showSection('delete-confirmation');
}

function showPostDetail(postId) {
    fetch(`/${postId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.post) {
                document.querySelector('#post-detail h3').textContent = data.post.title;
                document.querySelector('#post-detail p').textContent = data.post.body;
                showSection('post-detail');
            }
        });
}

function handleFormSubmission(form) {
  const formData = new FormData(form);
  fetch(form.action, {
      method: form.method,
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'success') {
          if (data.redirect_url) {
              window.location.href = data.redirect_url; // Redirect after deletion
          } else {
              alert('Operation successful');
              location.reload();
          }
      } else {
          alert('Error: ' + JSON.stringify(data.errors));
      }
  });
}
