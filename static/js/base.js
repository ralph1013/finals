console.log("TRY NGA");
document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
  
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
  deleteForm.action = `/blogs/${postId}/`; 
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
              window.location.href = data.redirect_url;
          } else {
              alert('Operation successful');
              location.reload();
          }
      } else {
          alert('Error: ' + JSON.stringify(data.errors));
      }
  });
}
document.querySelectorAll('.day').forEach(day => {
  day.addEventListener('mouseover', function() {
      const dayNum = this.getAttribute('data-day');
      const monthNum = this.getAttribute('data-month');
      const yearNum = this.getAttribute('data-year');
      
      fetch(`/appointments/?day=${dayNum}&month=${monthNum}&year=${yearNum}`)
          .then(response => response.json())
          .then(data => {
              console.log(data); 
          });
  });
});

const tableRows = document.querySelectorAll('#appointmentsTable tbody tr');
let selectedRow = null;

tableRows.forEach(row => {
  row.addEventListener('click', function() {
    if (selectedRow) {
      selectedRow.classList.remove('highlight');
    }
    this.classList.add('highlight');
    selectedRow = this;

    document.getElementById('editButton').style.display = 'inline';
    document.getElementById('deleteButton').style.display = 'inline';
  });
});

document.getElementById('editButton').addEventListener('click', function() {
  if (selectedRow) {
    const appointmentId = selectedRow.getAttribute('data-id');
    window.location.href = `/appointments/edit/${appointmentId}/`;
  }
});

document.getElementById('deleteButton').addEventListener('click', function() {
  if (selectedRow) {
    const appointmentId = selectedRow.getAttribute('data-id');
    if (confirm('Are you sure you want to delete this appointment?')) {
      window.location.href = `/appointments/delete/${appointmentId}/`;
    }
  }
});