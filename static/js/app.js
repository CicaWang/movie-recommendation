// API基础URL
const API_BASE = '';

// DOM元素
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const modal = document.getElementById('movie-modal');
const closeBtn = document.querySelector('.close');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 设置今日日期
    const today = new Date();
    const dateStr = today.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    document.getElementById('today-date').textContent = dateStr;

    // 加载今日推荐
    loadDailyMovies();

    // 标签切换
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName);

            // 根据标签加载相应数据
            if (tabName === 'hot' && !document.getElementById('hot-movies').hasChildNodes()) {
                loadHotMovies();
            } else if (tabName === 'upcoming' && !document.getElementById('upcoming-movies').hasChildNodes()) {
                loadUpcomingMovies();
            }
        });
    });

    // 类型推荐按钮
    document.getElementById('get-recommendations').addEventListener('click', loadPreferenceMovies);

    // 模态框关闭
    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
});

// 切换标签
function switchTab(tabName) {
    tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    tabContents.forEach(content => {
        content.classList.toggle('active', content.id === tabName);
    });
}

// 加载今日推荐
async function loadDailyMovies() {
    const container = document.getElementById('daily-movies');
    const loading = document.getElementById('daily-loading');

    try {
        loading.classList.remove('hidden');
        const response = await fetch(`${API_BASE}/api/movies/daily`);
        const data = await response.json();

        if (data.success) {
            container.innerHTML = '';
            data.movies.forEach(movie => {
                container.appendChild(createMovieCard(movie));
            });
        } else {
            container.innerHTML = '<p class="error">加载失败，请稍后重试</p>';
        }
    } catch (error) {
        console.error('Error loading daily movies:', error);
        container.innerHTML = '<p class="error">网络错误，请检查连接</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

// 加载热门电影
async function loadHotMovies() {
    const container = document.getElementById('hot-movies');
    const loading = document.getElementById('hot-loading');

    try {
        loading.classList.remove('hidden');
        const response = await fetch(`${API_BASE}/api/movies/hot`);
        const data = await response.json();

        if (data.success) {
            container.innerHTML = '';
            data.movies.forEach(movie => {
                container.appendChild(createMovieCard(movie));
            });
        } else {
            container.innerHTML = '<p class="error">加载失败，请稍后重试</p>';
        }
    } catch (error) {
        console.error('Error loading hot movies:', error);
        container.innerHTML = '<p class="error">网络错误，请检查连接</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

// 加载即将上映
async function loadUpcomingMovies() {
    const container = document.getElementById('upcoming-movies');
    const loading = document.getElementById('upcoming-loading');

    try {
        loading.classList.remove('hidden');
        const response = await fetch(`${API_BASE}/api/movies/upcoming`);
        const data = await response.json();

        if (data.success) {
            container.innerHTML = '';
            data.movies.forEach(movie => {
                container.appendChild(createMovieCard(movie));
            });
        } else {
            container.innerHTML = '<p class="error">加载失败，请稍后重试</p>';
        }
    } catch (error) {
        console.error('Error loading upcoming movies:', error);
        container.innerHTML = '<p class="error">网络错误，请检查连接</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

// 加载类型偏好推荐
async function loadPreferenceMovies() {
    const container = document.getElementById('preference-movies');
    const loading = document.getElementById('preference-loading');

    // 获取选中的类型
    const selectedGenres = [];
    document.querySelectorAll('.genre-chip input:checked').forEach(input => {
        selectedGenres.push(input.value);
    });

    if (selectedGenres.length === 0) {
        alert('请至少选择一个类型');
        return;
    }

    try {
        loading.classList.remove('hidden');
        const response = await fetch(`${API_BASE}/api/movies/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ genres: selectedGenres })
        });
        const data = await response.json();

        if (data.success) {
            container.innerHTML = '';
            data.movies.forEach(movie => {
                container.appendChild(createMovieCard(movie));
            });
        } else {
            container.innerHTML = '<p class="error">加载失败，请稍后重试</p>';
        }
    } catch (error) {
        console.error('Error loading preference movies:', error);
        container.innerHTML = '<p class="error">网络错误，请检查连接</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

// 创建电影卡片
function createMovieCard(movie) {
    const card = document.createElement('div');
    card.className = 'movie-card';

    const posterUrl = movie.poster || 'https://via.placeholder.com/200x300?text=No+Poster';
    const rating = movie.rating ? movie.rating.toFixed(1) : 'N/A';
    const releaseYear = movie.release_date ? new Date(movie.release_date).getFullYear() : '';

    card.innerHTML = `
        <img src="${posterUrl}" alt="${movie.title}" class="movie-poster" onerror="this.src='https://via.placeholder.com/200x300?text=No+Poster'">
        <div class="movie-info">
            <div class="movie-title">${movie.title}</div>
            <div class="movie-meta">
                <span class="movie-rating">${rating}</span>
                <span class="movie-date">${releaseYear}</span>
            </div>
        </div>
    `;

    // 点击显示详情
    card.addEventListener('click', () => showMovieDetail(movie));

    return card;
}

// 显示电影详情
function showMovieDetail(movie) {
    const modalBody = document.getElementById('modal-body');
    const posterUrl = movie.poster || 'https://via.placeholder.com/400x600?text=No+Poster';
    const rating = movie.rating ? movie.rating.toFixed(1) : 'N/A';

    modalBody.innerHTML = `
        <img src="${posterUrl}" alt="${movie.title}" onerror="this.src='https://via.placeholder.com/400x600?text=No+Poster'">
        <h2>${movie.title}</h2>
        <p><strong>评分:</strong> ${rating} / 10</p>
        <p><strong>上映日期:</strong> ${movie.release_date || '未知'}</p>
        <p><strong>数据来源:</strong> ${movie.source}</p>
        <p><strong>简介:</strong></p>
        <p>${movie.overview || '暂无简介'}</p>
    `;

    modal.classList.remove('hidden');
}

// 错误提示样式
const style = document.createElement('style');
style.textContent = `
    .error {
        text-align: center;
        padding: 40px;
        color: #999;
        font-size: 1.1em;
    }
`;
document.head.appendChild(style);
