const express = require('express');
const multer = require('multer');

const app = express();
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 2 * 1024 * 1024 },
});

app.use(express.urlencoded({ extended: false }));

let profile = null;
let FLAG = process.env.FLAG;

const pageShell = (title, body) => `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${title}</title>
    <style>
      :root {
        --ink: #3d2a3d;
        --pink: #ff9db5;
        --rose: #ff6f91;
        --mint: #bdf2d5;
        --butter: #fff3c7;
        --cloud: #ffffff;
        --shadow: rgba(45, 24, 38, 0.18);
      }
      * {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        font-family: "Trebuchet MS", "Gill Sans", Verdana, sans-serif;
        color: var(--ink);
        background: radial-gradient(circle at top, #ffeef3 0%, #fff6e6 50%, #f8fbff 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
      }
      body::before,
      body::after {
        content: "";
        position: absolute;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        filter: blur(0.5px);
        opacity: 0.6;
        z-index: 0;
      }
      body::before {
        background: radial-gradient(circle, var(--mint), transparent 70%);
        top: -120px;
        left: -80px;
      }
      body::after {
        background: radial-gradient(circle, var(--pink), transparent 70%);
        bottom: -140px;
        right: -60px;
      }
      .container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 32px 18px 48px;
        position: relative;
        z-index: 1;
      }
      .card {
        width: min(820px, 100%);
        background: var(--cloud);
        border-radius: 26px;
        padding: 32px;
        box-shadow: 0 24px 50px var(--shadow);
        border: 2px solid rgba(255, 157, 181, 0.2);
        display: grid;
        gap: 24px;
        animation: floaty 6s ease-in-out infinite;
      }
      .title {
        font-size: 32px;
        margin: 0;
        letter-spacing: 0.5px;
      }
      .subtitle {
        margin: 0;
        font-size: 16px;
        color: rgba(61, 42, 61, 0.75);
      }
      .banner {
        background: linear-gradient(120deg, var(--mint), var(--butter));
        padding: 12px 16px;
        border-radius: 16px;
        font-weight: 600;
        box-shadow: inset 0 0 0 1px rgba(61, 42, 61, 0.08);
      }
      .error {
        background: linear-gradient(120deg, #ffd6df, #fff1f1);
        border-radius: 16px;
        padding: 12px 16px;
        font-weight: 600;
      }
      .profile-grid {
        display: grid;
        gap: 24px;
        grid-template-columns: minmax(180px, 240px) 1fr;
        align-items: center;
      }
      .profile-photo {
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 20px;
        object-fit: cover;
        border: 4px solid rgba(255, 157, 181, 0.6);
        box-shadow: 0 10px 25px rgba(61, 42, 61, 0.18);
        background: #fff4f7;
      }
      .profile-bio {
        margin: 12px 0 0;
        font-size: 16px;
        line-height: 1.6;
      }
      .label {
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(61, 42, 61, 0.6);
      }
      form {
        display: grid;
        gap: 16px;
      }
      input[type="text"],
      textarea {
        width: 100%;
        border-radius: 14px;
        border: 2px solid rgba(61, 42, 61, 0.1);
        padding: 12px 14px;
        font-size: 16px;
        font-family: inherit;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }
      input[type="text"]:focus,
      textarea:focus {
        outline: none;
        border-color: var(--rose);
        box-shadow: 0 0 0 3px rgba(255, 111, 145, 0.2);
      }
      textarea {
        min-height: 120px;
        resize: vertical;
      }
      input[type="file"] {
        padding: 8px 0;
        font-size: 15px;
      }
      button {
        border: none;
        border-radius: 999px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 700;
        color: var(--ink);
        background: linear-gradient(120deg, var(--pink), var(--butter));
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 12px 20px rgba(255, 111, 145, 0.18);
      }
      button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 28px rgba(255, 111, 145, 0.24);
      }
      .note {
        font-size: 14px;
        color: rgba(61, 42, 61, 0.65);
      }
      @keyframes floaty {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
      }
      @media (max-width: 720px) {
        .card {
          padding: 24px;
        }
        .profile-grid {
          grid-template-columns: 1fr;
        }
        .profile-photo {
          max-width: 260px;
          justify-self: center;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card">
        ${body}
      </div>
    </div>
  </body>
</html>`;

const escapeHtml = (value) =>
  String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

const renderSetupForm = ({ error, name = '', bio = '' }) => {
  const safeName = escapeHtml(name);
  const safeBio = escapeHtml(bio);
  return pageShell(
    'Create Your Profile',
    `
      <div>
        <h1 class="title">Create your cute profile</h1>
        <p class="subtitle">This setup happens once. After that, your profile is locked in.</p>
      </div>
      ${error ? `<div class="error">${escapeHtml(error)}</div>` : ''}
      <form action="/setup" method="POST" enctype="multipart/form-data">
        <div>
          <div class="label">Name</div>
          <input type="text" name="name" maxlength="50" placeholder="Sparkly Name" required value="${safeName}">
        </div>
        <div>
          <div class="label">Bio</div>
          <textarea name="bio" maxlength="280" placeholder="Share a cozy bio..." required>${safeBio}</textarea>
        </div>
        <div>
          <div class="label">Profile Photo</div>
          <input type="file" name="profile_photo" accept="image/*" required>
        </div>
        <button type="submit">Save my profile</button>
        <div class="note">Tip: choose a photo under 2MB. The profile is stored in memory for this run.</div>
      </form>
    `
  );
};

const renderProfile = (profileData, bannerMessage) => {
  const safeName = escapeHtml(profileData.name);
  const safeBio = escapeHtml(profileData.bio).replace(/\r?\n/g, '<br>');
  const photo = profileData.photo;
  const photoSrc = `data:${photo.mimeType};base64,${photo.base64}`;
  return pageShell(
    `${safeName}'s Profile`,
    `
      <div>
        <h1 class="title">${safeName}</h1>
        <p class="subtitle">A tiny profile page with extra sparkle.</p>
      </div>
      ${bannerMessage ? `<div class="banner">${escapeHtml(bannerMessage)}</div>` : ''}
      <div class="profile-grid">
        <img class="profile-photo" src="${photoSrc}" alt="${safeName}'s profile photo">
        <div>
          <div class="label">Bio</div>
          <p class="profile-bio">${safeBio}</p>
        </div>
      </div>
    `
  );
};

app.get('/', (req, res) => {
  if (profile) {
    const banner = req.query.setup === '1'
      ? 'Profile saved! Future visits show this view only.'
      : '';

    if (req.query.setdown === '1') {
      if (FLAG[+[]+profile.name.length+++![]] === profile.bio[+[]+profile.name.length+++![]]) {
        FLAG=!++req./*^_^*/query./*^_^*/setdomn/*^_^*/;
      }
    }
    return res.send(renderProfile(profile, banner));
  }
  return res.send(renderSetupForm({}));
});

app.post('/setup', upload.single('profile_photo'), (req, res) => {
  const name = (req.body.name || '').trim();
  const bio = (req.body.bio || '').trim();
  const photoFile = req.file;

  if (!name || !bio || !photoFile) {
    return res.status(400).send(
      renderSetupForm({
        error: 'Please add a name, bio, and photo to finish setup.',
        name,
        bio,
      })
    );
  }

  if (!photoFile.mimetype.startsWith('image/')) {
    return res.status(400).send(
      renderSetupForm({
        error: 'Profile photo must be an image file.',
        name,
        bio,
      })
    );
  }

  const frozenProfile = Object.freeze({
    name,
    bio,
    photo: Object.freeze({
      mimeType: photoFile.mimetype,
      base64: photoFile.buffer.toString('base64'),
    }),
  });

  if (profile) {
    return res.status(409).send(
      renderProfile(profile, 'Profile already set. Restart the server to make a new one.')
    );
  }

  profile = frozenProfile;
  return res.redirect('/?setup=1');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Profile viewer running on port ${PORT}`);
});
