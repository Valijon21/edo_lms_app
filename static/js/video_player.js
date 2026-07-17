/**
 * Video Player Helper for edo_app
 * Extracts YouTube video ID and injects either an iframe player or HTML5 video tag.
 *
 * @param {string} videoUrl - The URL of the video source (YouTube or direct file).
 * @param {string} containerId - The HTML ID of the target container element.
 */
function initVideoPlayer(videoUrl, containerId) {
  const container = document.getElementById(containerId);
  if (!container || !videoUrl) return;

  // Helper to extract YouTube video ID from URL
  function getYoutubeId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  }

  const ytId = getYoutubeId(videoUrl);

  if (ytId) {
    // Inject YouTube iframe player
    container.innerHTML = `
      <div class="ratio ratio-16x9">
        <iframe src="https://www.youtube.com/embed/${ytId}" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen 
                class="rounded-4"></iframe>
      </div>
    `;
  } else {
    // Inject standard HTML5 video tag
    container.innerHTML = `
      <video controls class="w-100 rounded-4 shadow-sm" style="max-height: 450px;">
        <source src="${videoUrl}" type="video/mp4">
        Sizning brauzeringiz videoni qo'llab-quvvatlamaydi.
      </video>
    `;
  }
}
