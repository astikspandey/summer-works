const welcomeScreen = document.getElementById("welcome-screen");
const petNameScreen = document.getElementById("pet-name-screen");
const mainApp = document.getElementById("main-app");

const userNameInput = document.getElementById("user-name");
const userNameDisplay = document.getElementById("display-user-name");
const userNameMain = document.getElementById("display-user-name-main");

const petNameInput = document.getElementById("pet-name");
const petNameDisplay = document.getElementById("pet-display-name");

const userNameForm = document.getElementById("user-name-form");
if (userNameForm && userNameInput && userNameDisplay && userNameMain && welcomeScreen && petNameScreen) {
  userNameForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = userNameInput.value.trim();
    if (name) {
      userNameDisplay.textContent = name;
      userNameMain.textContent = name;
      welcomeScreen.style.display = "none";
      petNameScreen.style.display = "block";
      document.body.classList.remove('welcome-bg');
      // Cute transition: animate a heart
      showTransitionHeart();
    }
  });
}

const petInfoForm = document.getElementById("pet-info-form");
if (petInfoForm && petNameInput && petNameDisplay && petNameScreen && mainApp) {
  petInfoForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const petName = petNameInput.value.trim();
    if (petName) {
      petNameDisplay.textContent = petName;
      petNameScreen.style.display = "none";
      mainApp.style.display = "block";
      // Cute transition: animate a paw
      showTransitionPaw();
    }
  });
}

const petForm = document.getElementById("pet-form");
if (petForm) {
  petForm.addEventListener("submit", (e) => {
    e.preventDefault();
    // Gather all pet details
    const type = document.getElementById("pet-type")?.value || "";
    const breed = document.getElementById("pet-breed")?.value || "";
    const age = document.getElementById("pet-age")?.value || "";
    const genderRadio = document.querySelector('input[name="pet-gender"]:checked');
    const gender = genderRadio ? genderRadio.value : "";
    const color = document.getElementById("pet-color")?.value || "";
    const fav = document.getElementById("pet-fav")?.value || "";
    const photo = document.getElementById("pet-photo")?.value || "";
    const notes = document.getElementById("pet-notes")?.value || "";
    const name = document.getElementById("pet-name")?.value || "";

    // Save pet to localStorage
    let pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
    const feedingLog = [];
    const petObj = { name, type, breed, age, gender, color, fav, photo, notes, feedingLog, dailyChecklist: [] };
    pets.push(petObj);
    localStorage.setItem('trackifyPets', JSON.stringify(pets));

    // Show confirmation message
    const msg = document.getElementById('pet-added-message');
    if (msg) {
      msg.textContent = 'Pet added! You can now see it in the My Pets section.';
      msg.style.display = 'block';
      setTimeout(() => { msg.style.display = 'none'; }, 2000);
    }

    // Update My Pets section immediately
    if (typeof renderMyPets === 'function') renderMyPets();

    showPetProfile(petObj);
  });
}


function showPetProfile(pet, idx = null) {
  currentPetIdx = idx;

  // Theme logic
  let themeClass = "theme-other";
  if ((pet.gender === "female" && (pet.type === "cat" || pet.type === "rabbit")) || pet.gender === "female") themeClass = "theme-girl";
  else if ((pet.gender === "male" && (pet.type === "dog" || pet.type === "bird")) || pet.gender === "male") themeClass = "theme-boy";

  const profile = document.getElementById("pet-profile");
  profile.classList.remove("theme-girl", "theme-boy", "theme-other");
  profile.classList.add(themeClass);
  document.getElementById("profile-name").textContent = pet.name || "My Pet";
  document.getElementById("profile-breed").textContent = pet.breed || "-";
  document.getElementById("profile-age").textContent = pet.age ? `${pet.age} years` : "-";
  document.getElementById("profile-color").textContent = pet.color || "-";
  document.getElementById("profile-fav").textContent = pet.fav || "-";
  document.getElementById("profile-notes").textContent = pet.notes || "-";

  // Gender and type icons
  let typeIcon = "✨", genderIcon = "✨";
  if (pet.type === "dog") typeIcon = "🐶";
  if (pet.type === "cat") typeIcon = "🐱";
  if (pet.type === "rabbit") typeIcon = "🐰";
  if (pet.type === "bird") typeIcon = "🐦";
  if (pet.gender === "female") genderIcon = "♀️";
  if (pet.gender === "male") genderIcon = "♂️";
  document.getElementById("profile-type-gender").innerHTML = `<span style='font-size:2rem;'>${typeIcon}</span> <span style='font-size:1.5rem;'>${genderIcon}</span>`;

  // Photo (circular)
  const profilePhoto = document.getElementById("profile-photo");
  if (pet.photo && pet.photo.trim() !== "") {
    // Try to load the image first
    const img = new window.Image();
    img.onload = function() {
      profilePhoto.style.backgroundImage = `url('${pet.photo}')`;
      profilePhoto.textContent = "";
    };
    img.onerror = function() {
      profilePhoto.style.backgroundImage = "none";
      profilePhoto.textContent = typeIcon;
    };
    img.src = pet.photo;
  } else {
    profilePhoto.style.backgroundImage = "none";
    profilePhoto.textContent = typeIcon;
  }

  document.getElementById("main-app").style.display = "none";
  document.getElementById("pet-profile").classList.remove("hidden");
}

// --- Daily Checklist Logic ---
let currentPetIdx = null;

function renderChecklist(pet) {
  const checklistUl = document.getElementById('daily-checklist');
  checklistUl.innerHTML = '';
  if (!pet.dailyChecklist) pet.dailyChecklist = [];
  pet.dailyChecklist.forEach((item, idx) => {
    const li = document.createElement('li');
    li.innerHTML = `<input type="checkbox" ${item.checked ? 'checked' : ''} data-idx="${idx}"> ${item.text}`;
    checklistUl.appendChild(li);
  });
}

document.getElementById('add-checklist-item-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const input = document.getElementById('checklist-item-input');
  const text = input.value.trim();
  if (!text) return;
  let pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  if (currentPetIdx === null) return;
  pets[currentPetIdx].dailyChecklist = pets[currentPetIdx].dailyChecklist || [];
  pets[currentPetIdx].dailyChecklist.push({ text, checked: false });
  localStorage.setItem('trackifyPets', JSON.stringify(pets));
  renderChecklist(pets[currentPetIdx]);
  input.value = '';
});

document.getElementById('daily-checklist').addEventListener('change', function(e) {
  if (e.target.tagName === 'INPUT' && e.target.type === 'checkbox') {
    let pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
    if (currentPetIdx === null) return;
    const idx = parseInt(e.target.getAttribute('data-idx'));
    pets[currentPetIdx].dailyChecklist[idx].checked = e.target.checked;
    localStorage.setItem('trackifyPets', JSON.stringify(pets));
  }
});

// My Pets page logic
function renderMyPets() {
  let pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const list = document.getElementById('my-pets-list');
  list.innerHTML = '';
  if (pets.length === 0) {
    list.innerHTML = '<p>No pets added yet.</p>';
    return;
  }
  pets.forEach((pet, idx) => {
    const card = document.createElement('div');
    card.className = 'pet-card';
    card.innerHTML = `
      <div class="pet-card-photo" style="background-image:url('${pet.photo || ''}');">${!pet.photo ? (pet.type === 'dog' ? '🐶' : pet.type === 'cat' ? '🐱' : pet.type === 'rabbit' ? '🐰' : pet.type === 'bird' ? '🐦' : '✨') : ''}</div>
      <div class="pet-card-info">
        <h3>${pet.name}</h3>
        <p>${pet.breed || ''}</p>
        <button class="care-btn" onclick="window.showPetProfileFromList(${idx})">View</button>
      </div>
    `;
    list.appendChild(card);
  });
}
window.showPetProfileFromList = function(idx) {
  let pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  if (pets[idx]) showPetProfile(pets[idx], idx);
  document.getElementById('my-pets-page').classList.add('hidden');
}

document.getElementById('view-all-pets').onclick = function() {
  renderMyPets();
  document.getElementById('main-app').style.display = 'none';
  document.getElementById('my-pets-page').classList.remove('hidden');
};
document.getElementById('to-care-page').onclick = function() {
  document.getElementById('pet-profile').classList.add('hidden');
  document.getElementById('pet-care').classList.remove('hidden');
  // Render checklist for current pet
  let pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  if (currentPetIdx !== null && pets[currentPetIdx]) {
    renderChecklist(pets[currentPetIdx]);
  }
};
document.getElementById('back-to-main2').onclick = function() {
  document.getElementById('my-pets-page').classList.add('hidden');
  document.getElementById('main-app').style.display = 'block';
};

document.addEventListener('DOMContentLoaded', function() {
  const user = localStorage.getItem('trackifyUser');
  if (user) {
    document.getElementById('welcome-screen').style.display = 'none';
    document.getElementById('pet-name-screen').style.display = 'none';
    document.getElementById('main-app').style.display = 'block';
    document.body.classList.remove('welcome-bg');
  } else {
    document.body.classList.add('welcome-bg');
  }
});

document.getElementById("back-to-main").onclick = () => {
  document.getElementById("pet-profile").classList.add("hidden");
  document.getElementById("main-app").style.display = "block";
};

// Pet Care & Logs navigation
const carePage = document.getElementById("pet-care");
const profilePage = document.getElementById("pet-profile");
const toCareBtn = document.getElementById("to-care-page");
const backToProfileBtn = document.getElementById("back-to-profile");
if (toCareBtn && carePage && profilePage) {
  toCareBtn.onclick = () => {
    profilePage.classList.add("hidden");
    carePage.classList.remove("hidden");
    renderFeedingLog();
    renderVetLog();
    renderReminders();
  };
}
if (backToProfileBtn && carePage && profilePage) {
  backToProfileBtn.onclick = () => {
    carePage.classList.add("hidden");
    profilePage.classList.remove("hidden");
  };
}

// --- Feeding Log Modal Logic ---
const feedingModal = document.getElementById('feeding-modal');
const addFeedingBtn = document.getElementById('add-feeding');
const closeFeedingModal = document.getElementById('close-feeding-modal');
addFeedingBtn.onclick = () => { feedingModal.classList.remove('hidden'); };
closeFeedingModal.onclick = () => { feedingModal.classList.add('hidden'); };
document.getElementById('feeding-form').onsubmit = function(e) {
  e.preventDefault();
  if (currentPetIdx === null) return;
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const pet = pets[currentPetIdx];
  if (!pet.feedingLog) pet.feedingLog = [];
  pet.feedingLog.push({
    date: document.getElementById('feeding-date').value,
    food: document.getElementById('feeding-food').value,
    quantity: document.getElementById('feeding-quantity').value,
    notes: document.getElementById('feeding-notes').value
  });
  localStorage.setItem('trackifyPets', JSON.stringify(pets));
  feedingModal.classList.add('hidden');
  this.reset();
  renderFeedingLog();
};
function renderFeedingLog() {
  if (currentPetIdx === null) return;
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const pet = pets[currentPetIdx];
  const log = pet.feedingLog || [];
  const ul = document.getElementById('feeding-log');
  ul.innerHTML = '';
  log.slice().reverse().forEach(entry => {
    const li = document.createElement('li');
    li.innerHTML = `<b>${entry.date ? new Date(entry.date).toLocaleString() : ''}</b> - <b>${entry.food}</b> (${entry.quantity})<br><small>${entry.notes || ''}</small>`;
    ul.appendChild(li);
  });
}

// --- Vet Visit Modal Logic ---
const vetModal = document.getElementById('vet-modal');
const addVetBtn = document.getElementById('add-vet');
const closeVetModal = document.getElementById('close-vet-modal');
addVetBtn.onclick = () => { vetModal.classList.remove('hidden'); };
closeVetModal.onclick = () => { vetModal.classList.add('hidden'); };
document.getElementById('vet-form').onsubmit = function(e) {
  e.preventDefault();
  if (currentPetIdx === null) return;
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const pet = pets[currentPetIdx];
  if (!pet.vetLog) pet.vetLog = [];
  pet.vetLog.push({
    date: document.getElementById('vet-date').value,
    reason: document.getElementById('vet-reason').value,
    cost: document.getElementById('vet-cost').value,
    meds: document.getElementById('vet-meds').value,
    notes: document.getElementById('vet-notes').value
  });
  localStorage.setItem('trackifyPets', JSON.stringify(pets));
  vetModal.classList.add('hidden');
  this.reset();
  renderVetLog();
};
function renderVetLog() {
  if (currentPetIdx === null) return;
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const pet = pets[currentPetIdx];
  const log = pet.vetLog || [];
  const ul = document.getElementById('vet-log');
  ul.innerHTML = '';
  log.slice().reverse().forEach(entry => {
    const li = document.createElement('li');
    li.innerHTML = `<b>${entry.date ? new Date(entry.date).toLocaleDateString() : ''}</b> - <b>${entry.reason}</b> (₹${entry.cost || '0'})<br><small>Meds: ${entry.meds || '-'}<br>${entry.notes || ''}</small>`;
    ul.appendChild(li);
  });
}

// --- Reminder Modal Logic ---
const reminderModal = document.getElementById('reminder-modal');
const addReminderBtn = document.getElementById('add-reminder');
const closeReminderModal = document.getElementById('close-reminder-modal');
addReminderBtn.onclick = () => { reminderModal.classList.remove('hidden'); };
closeReminderModal.onclick = () => { reminderModal.classList.add('hidden'); };
document.getElementById('reminder-form').onsubmit = function(e) {
  e.preventDefault();
  if (currentPetIdx === null) return;
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const pet = pets[currentPetIdx];
  if (!pet.reminders) pet.reminders = [];
  pet.reminders.push({
    text: document.getElementById('reminder-text').value,
    date: document.getElementById('reminder-date').value
  });
  localStorage.setItem('trackifyPets', JSON.stringify(pets));
  reminderModal.classList.add('hidden');
  this.reset();
  renderReminders();
};
function renderReminders() {
  if (currentPetIdx === null) return;
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const pet = pets[currentPetIdx];
  const log = pet.reminders || [];
  const ul = document.getElementById('reminders-list');
  ul.innerHTML = '';
  log.slice().reverse().forEach(entry => {
    const li = document.createElement('li');
    li.innerHTML = `<b>${entry.text}</b>${entry.date ? ` <span style='color:#6c5b7b'>(at ${new Date(entry.date).toLocaleString()})</span>` : ''}`;
    ul.appendChild(li);
  });
}
// Close modals on overlay click
[...document.querySelectorAll('.modal')].forEach(modal => {
  modal.addEventListener('click', function(e) {
    if (e.target === modal) modal.classList.add('hidden');
  });
});


// Add New Pet button logic
const addNewPetBtn = document.getElementById("add-new-pet");
if (addNewPetBtn) {
  addNewPetBtn.onclick = () => {
    // Reset pet form fields
    document.getElementById("pet-form").reset();
    // Reset pet name input and display (if needed)
    document.getElementById("pet-name").value = "";
    document.getElementById("pet-display-name").textContent = "";
    // Show pet name screen for new entry
    document.getElementById("main-app").style.display = "none";
    document.getElementById("pet-name-screen").style.display = "block";
  };
}

// --- All Logs Page Logic ---
const viewAllLogsBtn = document.getElementById('view-all-logs');
const allLogsPage = document.getElementById('all-logs-page');
// Removed redeclaration of mainApp here. Use the one declared at the top of the file.
const backToMainLogsBtn = document.getElementById('back-to-main-logs');

if (viewAllLogsBtn) {
  viewAllLogsBtn.onclick = function() {
    if (mainApp) mainApp.style.display = 'none';
    if (allLogsPage) allLogsPage.classList.remove('hidden');
    renderAllLogs();
  };
}
if (backToMainLogsBtn) {
  backToMainLogsBtn.onclick = function() {
    if (allLogsPage) allLogsPage.classList.add('hidden');
    if (mainApp) mainApp.style.display = 'block';
  };
}

function renderAllLogs() {
  const pets = JSON.parse(localStorage.getItem('trackifyPets') || '[]');
  const feedingDiv = document.getElementById('all-feeding-logs');
  const vetDiv = document.getElementById('all-vet-logs');
  feedingDiv.innerHTML = '';
  vetDiv.innerHTML = '';
  if (!pets.length) {
    feedingDiv.innerHTML = '<p>No pets or logs found.</p>';
    vetDiv.innerHTML = '<p>No pets or logs found.</p>';
    return;
  }
  pets.forEach(pet => {
    // Feeding logs
    if (pet.feedingLog && pet.feedingLog.length) {
      const fSection = document.createElement('div');
      fSection.innerHTML = `<h4>${pet.name}</h4>`;
      const ul = document.createElement('ul');
      pet.feedingLog.forEach(entry => {
        const li = document.createElement('li');
        li.innerHTML = `<b>${entry.date ? new Date(entry.date).toLocaleString() : ''}</b> - <b>${entry.food}</b> (${entry.quantity})<br><small>${entry.notes || ''}</small>`;
        ul.appendChild(li);
      });
      fSection.appendChild(ul);
      feedingDiv.appendChild(fSection);
    }
    // Vet logs
    if (pet.vetLog && pet.vetLog.length) {
      const vSection = document.createElement('div');
      vSection.innerHTML = `<h4>${pet.name}</h4>`;
      const ul = document.createElement('ul');
      pet.vetLog.forEach(entry => {
        const li = document.createElement('li');
        li.innerHTML = `<b>${entry.date ? new Date(entry.date).toLocaleDateString() : ''}</b> - <b>${entry.reason}</b> (₹${entry.cost || '0'})<br><small>Meds: ${entry.meds || '-'}<br>${entry.notes || ''}</small>`;
        ul.appendChild(li);
      });
      vSection.appendChild(ul);
      vetDiv.appendChild(vSection);
    }
  });
}



// 🎵 Music Controls
const music = document.getElementById("bg-music");
const musicToggle = document.getElementById("music-toggle");
const musicPanel = document.getElementById("music-controls");
const vibeSelect = document.getElementById("music-vibe");

const musicTracks = {
  lullaby: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", // Test MP3
  piano:   "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
  ambient: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
  lofi:    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
};

// Store current vibe
let currentVibe = 'lullaby';
vibeSelect.value = 'lullaby';
vibeSelect.addEventListener("change", () => {
  currentVibe = vibeSelect.value;
});

document.getElementById("play-btn").onclick = () => {
  // Always set src just before play for best browser compatibility
  music.src = musicTracks[currentVibe];
  music.load();
  music.play().catch((err) => {
    alert("Couldn't play music.\n\n1. Make sure your volume is up.\n2. Try clicking Play again.\n3. Some browsers block music until you interact with the page.\n4. If using Brave/Chrome, check if the shield or site settings block autoplay.\n\nError: " + err.message);
  });
};
document.getElementById("pause-btn").onclick = () => music.pause();
document.getElementById("mute-btn").onclick = () => music.muted = !music.muted;
document.getElementById("stop-btn").onclick = () => {
  music.pause();
  music.currentTime = 0;
};
document.getElementById("volume-slider").oninput = (e) => {
  music.volume = e.target.value;
};

musicToggle.addEventListener("click", () => {
  musicPanel.classList.toggle("hidden");
  // Animate the music note for feedback
  musicToggle.classList.add("bounce");
  setTimeout(() => musicToggle.classList.remove("bounce"), 600);
});

// Add bounce animation via JS (CSS required in styles2.css)
// Cute transition heart
function showTransitionHeart() {
  const heart = document.createElement("div");
  heart.textContent = "💖";
  heart.style.position = "fixed";
  heart.style.left = "50%";
  heart.style.top = "50%";
  heart.style.transform = "translate(-50%, -50%) scale(1.5)";
  heart.style.fontSize = "3rem";
  heart.style.zIndex = 99;
  heart.style.transition = "opacity 0.7s, transform 0.7s";
  document.body.appendChild(heart);
  setTimeout(() => {
    heart.style.opacity = 0;
    heart.style.transform = "translate(-50%, -60%) scale(2.1)";
    setTimeout(() => heart.remove(), 700);
  }, 400);
}
// Cute transition paw
function showTransitionPaw() {
  const paw = document.createElement("div");
  paw.textContent = "🐾";
  paw.style.position = "fixed";
  paw.style.left = "50%";
  paw.style.top = "55%";
  paw.style.transform = "translate(-50%, -50%) scale(1.5)";
  paw.style.fontSize = "2.7rem";
  paw.style.zIndex = 99;
  paw.style.transition = "opacity 0.7s, transform 0.7s";
  document.body.appendChild(paw);
  setTimeout(() => {
    paw.style.opacity = 0;
    paw.style.transform = "translate(-50%, -60%) scale(2.1)";
    setTimeout(() => paw.remove(), 700);
  }, 400);
}

