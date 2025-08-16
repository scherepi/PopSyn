// @ts-nocheck
(function () {
	const queryInput = document.getElementById('song-query');
	const searchBtn = document.getElementById('search-btn');
	const songResult = document.getElementById('song-result');
	const coverPh = document.getElementById('cover-ph');
	const coverImg = document.getElementById('cover');
	const titleEl = document.getElementById('title');
	const artistEl = document.getElementById('artist');
	const addSynBtn = document.getElementById('add-syn-btn');
	const synModal = document.getElementById('syn-modal');
	const closeModal = document.getElementById('close-modal');
	const modalColorSwatch = document.getElementById('modal-color-swatch');
	const modalColorInput = document.getElementById('modal-color-input');
	const synDescription = document.getElementById('syn-description');
	const confirmAdd = document.getElementById('confirm-add');

	let latestController = null;
	let currentSongData = null;

	function getArtistName(r) {
		const ac0 = r['artist-credit'] && r['artist-credit'][0];
		return (ac0 && (ac0.name || (ac0.artist && ac0.artist.name))) || '';
	}
	async function searchMusicBrainz(query) {
		if (latestController) latestController.abort();
		latestController = new AbortController();
		const url = `https://musicbrainz.org/ws/2/recording?query=${encodeURIComponent(query)}&fmt=json&limit=25&inc=artist-credits+releases`;
		const res = await fetch(url, {
			headers: { 'Accept': 'application/json' },
			signal: latestController.signal,
			cache: 'no-store'
		});
		if (!res.ok) throw new Error('search failed');
		const data = await res.json();
		return data.recordings || [];
	}

	function chooseResult(ds) {
		const { title, artist, releaseId } = ds;
		if (!title || !artist) return;
		currentSongData = { title, artist, releaseId };
		titleEl.textContent = title;
		artistEl.textContent = artist;
		coverPh.classList.remove('hidden');
		coverImg.classList.add('hidden');
		if (releaseId) {
			coverImg.src = `https://coverartarchive.org/release/${releaseId}/front-500`;
			coverImg.onload = () => {
				coverPh.classList.add('hidden');
				coverImg.classList.remove('hidden');
			};
			coverImg.onerror = () => {
				coverPh.classList.remove('hidden');
				coverImg.classList.add('hidden');
			};
		}
		
		addSynBtn.classList.remove('hidden');
		songResult.classList.remove('hidden');
	}
	function openModal() {
		synModal.classList.add('flex');
		synModal.classList.remove('hidden');
		document.body.classList.add('modal-open');
		document.addEventListener('keydown', escKeyHandler);
	}
	function closeModalFunc() {
		synModal.classList.remove('flex');
		synModal.classList.add('hidden');
		document.body.classList.remove('modal-open');
		document.removeEventListener('keydown', escKeyHandler);
	}
	function updateModalSwatch(hex) { modalColorSwatch.style.backgroundColor = hex; }
	function handleAddSyn() {
		const selectedColor = modalColorInput.value;
		const description = synDescription.value.trim();
		const songInfo = currentSongData;
		closeModalFunc();
		const params = new URLSearchParams({ 
			artist: songInfo.artist, 
			title: songInfo.title,
			color: selectedColor,
			description: description
		});
		window.location.href = `/add?${params.toString()}`;
	}
	addSynBtn.addEventListener('click', openModal);
	closeModal.addEventListener('click', closeModalFunc);
	confirmAdd.addEventListener('click', handleAddSyn);
	function escKeyHandler(e) {
		if (e.key === 'Escape') {
			closeModalFunc();
		}
	}
	
	synModal.addEventListener('click', (e) => {
		if (e.target === synModal) {
			closeModalFunc();
		}
	});

	modalColorSwatch.addEventListener('click', () => modalColorInput.click());
	modalColorInput.addEventListener('input', (e) => updateModalSwatch(e.target.value));
	

	async function searchBestMatch(raw) {
		const recs = await searchMusicBrainz(raw);
		if (!recs.length) return null;
		let best = recs.find(r => Array.isArray(r.releases) && r.releases.length) || recs[0];
		const release = (best.releases && best.releases[0]) || null;
		return {
			title: best.title || raw,
			artist: getArtistName(best) || 'Unknown artist',
			releaseId: release ? release.id : ''
		};
	}

	async function handleSearch() {
		const q = (queryInput.value || '').trim();
		if (q.length < 2) { return; }
		try {
			const match = await searchBestMatch(q);
			if (!match) { songResult.classList.add('hidden'); return; }
			chooseResult(match);
		} catch (_) {
			songResult.classList.add('hidden');
		}
	}
	queryInput.addEventListener('keydown', (e) => {
		if (e.key === 'Enter') {
			e.preventDefault();
			handleSearch();
		}
	});
	searchBtn.addEventListener('click', handleSearch);
})();


