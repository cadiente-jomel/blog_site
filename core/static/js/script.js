function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

if (document.getElementById('comment-form')) {
    const form = document.getElementById('comment-form');
    let postPut = false;
    let curr_id;
    form.addEventListener('submit', (e) => {
        let m = [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'June',
            'July',
            'Aug',
            'Sept',
            'Oct',
            'Nov',
            'Dec',
        ];
        let date = new Date();
        let month = m[date.getDate()];
        let day = date.getDay();
        let year = date.getFullYear();
        let final = `${year} ${month} ${day}`;
        let url = '/api/comments/create/';
        let method = 'POST';
        e.preventDefault();
        let data = {
            comment: document.getElementById('comment-input').value,
            id: document.getElementById('p-id').value,
            user_profile: document.getElementById('u-img').value,
            // 'post': document.getElementById('post-title').innerText
        };
        if (postPut !== false) {
            url = `/api/comments/${curr_id}/update/`;
            method = 'PUT';
            data = {
                comment: document.getElementById('comment-input').value,
            };
            postPut = false;
        }
        postComment(method, url, data);
    });

    const postComment = async (method, url, data = {}) => {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            mode: 'same-origin',
            body: JSON.stringify(data),
        }).then((res) => {
            buildList();
            if (document.querySelector('.comment-input')) {
                let commentInput = document.querySelector('.comment-input');
                commentInput.style.marginBottom = '0';
                let toggle = document.getElementById('toggle-c');
                toggle.classList.add('toggle-c');
                commentInput.style.height = '25px';
            }
            let commentCount = document.querySelectorAll('.count-comment');
            let resText = document.querySelector('.c-res');
            let resCount = document.querySelector('#comment-main-container')
                .childElementCount;
            commentCount.forEach((comment) => {
                comment.textContent = resCount + 1;
            });
            resText.textContent =
                resCount <= 0
                    ? `Response (${resCount + 1})`
                    : `Responses (${resCount + 1})`;
            form.reset();
        });
    };

    const deleteItem = async (item) => {
        fetch(`/api/comments/${item.id}/delete/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        }).then((res) => {
            buildList();
            let commentCount = document.querySelectorAll('.count-comment');
            let resText = document.querySelector('.c-res');
            let resCount = document.querySelector('#comment-main-container');
            commentCount.forEach((comment) => {
                comment.textContent = resCount.childElementCount - 1;
            });
            resText.textContent =
                resCount.childElementCount <= 0
                    ? `Response (${resCount.childElementCount - 1})`
                    : `Responses (${resCount.childElementCount - 1})`;
        });
    };

    const buildList = async () => {
        let post_title = document.querySelector('.d-post-title').innerText;
        let comment_container = document.getElementById(
            'comment-main-container'
        );
        // let response = await fetch('/api/comments/');
        // let data = await response.json();
        const url = '/api/comments/';
        fetch(url)
            .then((res) => res.json())
            .then((data) => {
                let list = data;
                // console.log(list);
                var item_list = [];
                try {
                    let current = document.querySelectorAll(
                        `.comment-container`
                    );
                    current.forEach((el) => {
                        el.remove();
                    });
                } catch (err) {}
                for (let comment in list) {
                    if (post_title == list[comment].post) {
                        let item = `<div class="comment-container mb-4">
                          <div class="about-user-container mb-2" id="about-user-container${comment}">
                          <div class="about-user">
                            <div class="img-container img-container-c">
                              <img class="img-profile img-profile-c" src="${list[comment].user_profile}" alt="profile">
                            </div>
                            <div class="user-post-created">
                            <div class="user-info-container">
                              <div class="user-info">
                                <span>${list[comment].user}</span>
                              </div>
                            </div>
                            <div class="date-created-container">
                              <div class="data-created">
                                <span>${list[comment].created}</span>
                              </div>
                            </div>
                            </div>
                            </div>
                          </div>
                        
                        <div class="user-comment-container mb-3">
                          <div class="comment-detail">
                            <p>${list[comment].comment}</p>
                          </div>
                        </div> 
                      </div>
                      </div>`;

                        comment_container.innerHTML += item;
                        let curr_user = document.getElementById('c-user').value;
                        if (list[comment].user == curr_user) {
                            let comment_control = `<div class="dropdown  ml-auto">
                <button class="btn dropdown d-outline" type="button" id="dropdownMenuButton" data-toggle="dropdown">
                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-three-dots" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
              </svg>
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <a class="dropdown-item delete-comment">Delete</a>
                  <a class="dropdown-item edit-comment" >Edit</a>
                </div>
              </div>`;
                            let parent_container = document.getElementById(
                                `about-user-container${comment}`
                            );
                            parent_container.innerHTML += comment_control;
                            item_list.push(list[comment]);
                        }
                    }
                }
                btn_edit(item_list);
                btn_delete(item_list);
            });
    };

    const btn_delete = (item) => {
        let pos = 0;
        let delete_btn = document.querySelectorAll('.delete-comment');
        item.forEach((e) => {
            for (let i = 0; i < delete_btn.length; i++) {
                delete_btn[pos].addEventListener('click', () => {
                    deleteItem(e);
                });
                break;
            }
            pos += 1;
        });
    };

    const btn_edit = (item) => {
        let pos = 0;
        let edit_btn = document.querySelectorAll('.edit-comment');
        item.forEach((e) => {
            for (let i = 0; i < edit_btn.length; i++) {
                edit_btn[pos].addEventListener('click', () => {
                    commentInput = document.getElementById('comment-input');
                    commentInput.value = e.comment;
                    curr_id = e.id;
                    postPut = true;
                });
                break;
            }
            pos += 1;
        });
    };

    buildList();
}

if (document.querySelector('.sidebar-close')) {
    let sidebarClose = document.querySelector('.sidebar-close');
    let sidebarContainer = document.querySelector('.sidebar-container');
    let sidebar = document.querySelector('.sidebar');
    let innerSidebar = document.querySelector('.inner-sidebar-container');
    sidebarClose.addEventListener('click', () => {
        innerSidebar.style.backgroundColor = '';
        sidebar.style.right = '-414px';
        sidebarContainer.style.pointerEvents = 'none';
    });
}

const commentSec = () => {
    if (document.querySelector('.comment-input')) {
        let chatBtnList = document.querySelectorAll('.chat-btn');
        let toggle = document.getElementById('toggle-c');
        let commentInput = document.querySelector('.comment-input');
        let innerSidebar = document.querySelector('.inner-sidebar-container');
        let commentAdd = document.querySelector('.c-add');
        let cancelBtn = document.querySelector('.cancel-btn');
        chatBtnList.forEach((chatBtn) => {
            let a = 0;
            chatBtn.addEventListener('click', () => {
                let sidebarContainer = document.querySelector(
                    '.sidebar-container'
                );
                let sidebar = document.querySelector('.sidebar');
                // sidebarContainer.style.display = 'block';
                sidebarContainer.style.pointerEvents = 'auto';
                sidebar.style.right = '0px';
                innerSidebar.style.backgroundColor = '#686d76';

                // sidebar.style.transition = '2s ease-in'
            });
        });

        cancelBtn.addEventListener('click', () => {
            commentInput.blur;
            toggle.classList.add('toggle-c');
            commentInput.style.marginBottom = '0';
            commentInput.style.height = '25px';
            commentInput.value = '';
        });
        commentInput.addEventListener('focus', () => {
            commentInput.style.marginBottom = '10px';
            toggle.classList.remove('toggle-c');
            if (commentInput.value == '') {
                commentInput.style.height = '40px';
                commentInput.style.transition = '.2s ease-in-out';
                commentAdd.disabled = true;
                commentAdd.style.backgroundColor = '#BDDCBD';
                commentAdd.style.cursor = 'not-allowed';
            }
        });

        commentInput.addEventListener('keypress', () => {
            if (commentInput.value.length > 0) {
                commentAdd.disabled = false;
                commentAdd.style.backgroundColor = '#1a8917';
                commentAdd.style.cursor = 'pointer';
            } else {
                // commentInput.style.height = '40px'
                commentAdd.disabled = true;
                commentAdd.style.backgroundColor = '#BDDCBD';
                commentAdd.style.cursor = 'not-allowed';
            }
        });

        commentInput.addEventListener('blur', () => {
            if (commentInput.value == '') {
                commentInput.style.marginBottom = '0';
                commentInput.style.transition = '.2s ease-in-out';
                let toggle = document.getElementById('toggle-c');
                toggle.classList.add('toggle-c');
                commentInput.style.height = '25px';
            }
        });

        let likeFormList = document.querySelectorAll('.like-form');
        likeFormList.forEach((likeForm) => {
            likeForm.addEventListener('submit', (e) => {
                let j = 0;
                e.preventDefault();
                let url = likeForm.attributes.action.textContent;
                let post_slug = document.querySelectorAll('.post-slug');
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    data: {
                        post_slug: post_slug[j],
                    },
                })
                    .then((res) => {
                        return res.json();
                    })
                    .then((res) => {
                        let postCountList = document.querySelectorAll(
                            '.post-count'
                        );
                        let likeHeartList = document.querySelectorAll(
                            '.post-slug'
                        );
                        let i = 0;
                        likeHeartList.forEach((likeHeart) => {
                            if (res.is_like) {
                                postCountList[i].textContent =
                                    parseInt(postCountList[i].textContent) + 1;
                                likeHeart.innerHTML = `<svg aria-label="Unlike" class="_8-yf5 l-um" fill="#ed4956" height="24" viewBox="0 0 48 48" width="24"><path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>`;
                            } else {
                                postCountList[i].textContent =
                                    parseInt(postCountList[i].textContent) - 1;
                                likeHeart.innerHTML = `<svg aria-label="Like" class="_8-yf5 l-um" fill="#75757E" height="24" viewBox="0 0 48 48" width="24"><path d="M34.6 6.1c5.7 0 10.4 5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>`;
                            }
                            i += 1;
                        });
                    });
                j += 1;
            });
        });

        let title_c = document.querySelector('.d-post-title');
        if (isInViewport(title_c)) {
            let userInteraction = document.querySelector('.user-interaction');
            let pointEvents = document.querySelectorAll('.u-m');
            userInteraction.style.opacity = '0';
            pointEvents.forEach((el) => {
                el.style.pointerEvents = 'none';
            });
        }

        window.addEventListener('scroll', () => {
            let title = document.querySelector('.d-post-title');
            let userInteraction = document.querySelector('.user-interaction');
            let pointEvents = document.querySelectorAll('.u-m');

            if (!isInViewport(title)) {
                userInteraction.style.opacity = '1';
                pointEvents.forEach((el) => {
                    el.style.pointerEvents = 'auto';
                });
            } else {
                userInteraction.style.opacity = '0';
                pointEvents.forEach((el) => {
                    el.style.pointerEvents = 'none';
                });
            }
        });
    }
};

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.bottom >= 0 &&
        rect.left >= 0 &&
        rect.bottom <=
            (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <=
            (window.innerWidth || document.documentElement.clientWidth)
    );
}

function autoGrow(oField) {
    if (oField.scrollHeight > oField.clientHeight) {
        oField.style.height = oField.scrollHeight + 'px';
    }
}

function searchToggle() {
    let form = document.querySelector('.form-control');
    form.addEventListener('focus', () => {
        let searchContainer = document.querySelector('.search-container');
        searchContainer.classList.add('search-toggle');
    });
    form.addEventListener('blur', () => {
        let searchContainer = document.querySelector('.search-container');
        searchContainer.classList.remove('search-toggle');
    });

    // let userInput = document.querySelectorAll('.textInput')
    // userInput.forEach(el => {
    //     el.addEventListener('focus', () => {
    //         el.classList.add('search-toggle')
    //     })

    //     el.addEventListener('blur', () => {
    //         el.classList.remove('search-toggle')
    //     })
    // })
}

if (document.getElementById('div_id_body')) {
    let el = document.getElementById('div_id_body').childNodes[3].childNodes[1];

    el.style.maxWidth = 'none';
    el.style.border = '1px solid rgba(0, 0, 0, 0.425)';
    el.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.473)';
    let formArr = ['title', 'snippet', 'body'];

    formArr.forEach((form) => {
        let formLabel = document.getElementById(`div_id_${form}`).childNodes[1];
        formLabel.remove();
    });
}

// move this outside the scope
if (document.querySelectorAll('.book-form')) {
    let bookFormList = document.querySelectorAll('.book-form');
    bookFormList.forEach((bookForm) => {
        bookForm.addEventListener('click', (e) => {
            let i = 0;

            e.preventDefault();
            let url = bookForm.attributes.action.textContent;
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
            })
                .then((res) => {
                    return res.json();
                })
                .then((res) => {
                    let likeHeartList = document.querySelectorAll('.post-book');
                    likeHeartList.forEach((likeHeart) => {
                        if (document.querySelector('.post-title')) {
                            let post = document.querySelectorAll('.post-title')[
                                i
                            ].innerText;
                            if (post === res.post) {
                                checkBookMarked(res.isBookMarked, likeHeart);
                            }
                        } else {
                            checkBookMarked(res.isBookMarked, likeHeart);
                        }
                        i += 1;
                    });
                });
        });
    });

    const checkBookMarked = (is_True, bookmarkBtn) => {
        if (is_True) {
            bookmarkBtn.innerHTML = `<i class="fas fa-bookmark"></i>`;
        } else {
            bookmarkBtn.innerHTML = `<i class="far fa-bookmark"></i>`;
        }
    };
}

if ((dateContainer = document.querySelectorAll('#date-c'))) {
    let dateContainer = document.querySelectorAll('#date-c');
    dateContainer.forEach((date) => {
        let curr = date.textContent;
        date.textContent = curr.split(',')[0];
    });
}

const popup = () => {
    if (document.querySelector('.open-popup-btn')) {
        let popupBtn = document.querySelectorAll('.open-popup-btn');
        let dismissBtn = document.querySelectorAll('.dismiss-popup-btn');
        let i = 0;
        popupBtn.forEach((btn) => {
            btn.addEventListener('click', () => {
                document.querySelector('.popup').classList.add('active');
            });
            i += 1;
        });

        dismissBtn.forEach((dBtn) => {
            dBtn.addEventListener('click', () => {
                document.querySelector('.popup').classList.remove('active');
            });
            i += 1;
        });

        let forms = document.querySelectorAll('.f-form');

        forms.forEach((f_form) => {
            f_form.addEventListener('submit', (e) => {
                e.preventDefault();
                let url = f_form.attributes.action.textContent;
                fetch(url)
                    .then((res) => {
                        return res.json();
                    })
                    .then((res) => {
                        const htmlGenerator = (data, text) => {
                            let popupText = document.querySelector('.dismiss-btn')
                            let span = document.createElement('span')
                            span.classList.add('s-text')
                            span.textContent = text;
                            popupText.prepend(span)
                            let container = document.querySelector(
                                '.following-followers-container'
                            );
                            data.forEach((data) => {
                                container.innerHTML += `
                                <div class="user-profile">
                                <a href="/profile/${data['fields'].username}">
                                <div class="icon">
                                    <img class="author-profile" src="${data['additional fields']}" alt="">
                                </div>
                                <div class="description">
                                @${data['fields'].username}
                                </a>
                                </div>
                                </div>`
                                
                            ;
                            });
                        };

                        try {
                            let userprof = document.querySelectorAll(
                                '.user-profile'
                            );
                            userprof.forEach((u) => {
                                u.remove();
                            });
                            document.querySelector('.s-text').remove()
                        } catch (err) {}
                        if (res.following) {
                            htmlGenerator(res.following, 'Following');
                        } else {
                            htmlGenerator(res.followers, 'Followers');
                        }
                    });
            });
        });
    }
};


const follow = () => {
    if(document.querySelector('.follow')) {
        let anchor = document.querySelector('.follow')
        let url = anchor.href
        anchor.addEventListener('click', (e) => {
            e.preventDefault()
            fetch(url)
                .then(res => {
                    return res.json()
                })
                .then(res => {
                    if(res.data == 'Following') {
                        anchor.classList.remove('custom-nav')
                        anchor.classList.remove('create')
                        anchor.classList.add('file-btn')
                    } else {
                        anchor.classList.remove('file-btn')
                        anchor.classList.add('custom-nav')
                        anchor.classList.add('create')
                    }
                    anchor.textContent = res.data
                })
        })
    }
}

const removeCurrentData = () => {
    try {
        let removeData = document.querySelectorAll('.dashboard-data')
        removeData.forEach(el => {
            el.remove()
        })
        if (document.querySelector('.social-container-outer')) {
            document.querySelector('.social-container-outer').remove()
        }

        if (document.querySelector('.dash-comment-container')) {
            let commentData = document.querySelectorAll('.dash-comment-container')
            commentData.forEach(el => {
                el.remove();
            })
        }
    }
    catch {}
}

// slugify title
function slugify(text) {
    const from = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;"
    const to = "aaaaaeeeeeiiiiooooouuuunc------"
  
    const newText = text.split('').map(
      (letter, i) => letter.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i)))
  
    return newText
      .toString()                     // Cast to string
      .toLowerCase()                  // Convert the string to lowercase letters
      .trim()                         // Remove whitespace from both sides of a string
      .replace(/\s+/g, '-')           // Replace spaces with -
    //   .r(/&/g, '')           // Replace & with 'and'
      .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
      .replace(/\-\-+/g, '-');        // Replace multiple - with single -
  }

const dashboardDeletePostComment = (cls) => {
    // dashboard/delete/<str:category>/
    let deleteListener = document.querySelectorAll(`.${cls}`)
                        
                        deleteListener.forEach(btn => {
                            btn.addEventListener('click', () => {
                                let item = btn.parentElement.childNodes[0]
                                if (item.constructor.name === 'Text') {
                                    item = btn.parentElement.childNodes[1]
                                }

                                data = {
                                    what: cls
                                }

                                fetch(`/dashboard/delete/${item.value}/`, {
                                    method: 'POST',
                                    headers: {
                                        'X-CSRFToken': csrftoken,
                                        'Content-Type': 'application/json'
                                    }, body: JSON.stringify(data)
                                }).then(res => {
                                    return res.json()
                                }).then(data => {
                                    if (cls === 'edit-delete') {
                                        btn.parentElement.parentElement.remove();
                                    } else {
                                        btn.parentElement.parentElement.parentElement.remove();
                                    }
                                    console.log(data.message)
                                })
                                // if (cls === 'post-delete') {

                                // } else if (cls == 'edit-delete') {

                                // }
                            })
                        })
}



const dashboard = () => {
    if(document.querySelector('.children-list')) {
        let categoryList = document.querySelectorAll('.children-list')
        categoryList.forEach(category => {
            category.addEventListener('click', () => {
                categoryList.forEach(btn => {
                    if(btn !== category) {
                        btn.classList.remove('selected-toggle')
                    } else {
                        btn.classList.add('selected-toggle')
                    }
                })
            })
        })

        const helper = (el, str) => {
            return el.textContent.includes(str)
        }

        // try {
        //     let editURI = document.getElementById('id-edit').attributes[2].textContent
        //     editURI = editURI.substring(0, editURI.indexOf('/', 2) + 1)
        // }catch{}
        // try {
        //     let deleteURI = document.getElementById('id-delete').attributes[2].textContent
        //     deleteURI = deleteURI.substring(0, deleteURI.indexOf('/', 2) + 1)
        // }catch{}
        // try {
        //     let postURI = document.getElementById('id-post').attributes[2].textContent
        //     postURI = postURI.substring(0, postURI.indexOf('/', 2) + 1)
        // } catch (error) {
            
        // }
        // try {
        //     let socialURI = document.getElementById('id-soc').attributes[2].textContent
        //     socialURI = socialURI.substring(0, socialURI.indexOf('/', 2) + 1)
            
        // } catch (error) {
        // }
        
        
        let categoryBtn = document.querySelectorAll('.category-btn')
        let dataContainer = document.querySelector('.dashboard-container-inner')
        categoryBtn.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault()
                let url = btn.href
                let headerTitle = document.querySelector('.header-title')
                console.log(url)
                fetch(url)
                .then(res => {
                   
                    return res.json()
                })
                .then(res => {
                    let obj;
                    if (helper(btn, 'Post') || helper(btn, 'Draft')) {
                        removeCurrentData();
                        obj = JSON.parse(res.data)
                        obj.forEach(data => {
                            let container = document.createElement('div')
                            container.classList.add('dashboard-data')
                            container.classList.add('b-shadow')
                            container.classList.add('mb-3')
                            let innerData = document.createElement('div')
                            innerData.classList.add('data')
                            let title = document.createElement('div')
                            title.classList.add('title')
                            let  titleText = document.createElement('a')
                            titleText.textContent = `${data.fields.title.substring(0, 29)}...`
                                titleText.href = `/post/${data.fields.slug}`
                            title.appendChild(titleText)
                            innerData.appendChild(title)
                            let draft = document.createElement('div')
                            draft.classList.add('draft')
                            let draftText = document.createElement('a')
                            console.log('isDraft', data.fields.draft)
                            if (data.fields.draft === true) {
                                headerTitle.textContent = 'Draft'
                                draftText.textContent = 'Draft'
                                    draftText.href = `/edit-post/${data.fields.slug}`
                            } else {
                                headerTitle.textContent = 'Posts'
                                draftText.textContent = 'Published'
                                try {
                                    draftText.href = `/edit-post/${data.fields.slug}`
                                    
                                } catch (error) {
                                    
                                }
                            }
                            draft.appendChild(draftText)
                            innerData.appendChild(draft)
                            let controls = document.createElement('div')
                            controls.classList.add('controls')
                            const idHidden = document.createElement('input');
                            idHidden.type = 'hidden'
                            idHidden.value = data.fields.slug;
                            let deleteBtn = document.createElement('a')
                            deleteBtn.classList.add('post-delete')
                            deleteBtn.textContent = 'Delete'
                                // deleteBtn.href = `/delete-post/${data.fields.slug}`
                            let editBtn = document.createElement('a')
                            editBtn.classList.add('edit')
                            editBtn.textContent = 'Edit'
                           
                                editBtn.href = `/edit-post/${data.fields.slug}`
                            controls.appendChild(idHidden)
                            controls.appendChild(deleteBtn)
                            controls.appendChild(editBtn)
                            innerData.appendChild(controls)
                            container.appendChild(innerData)
                            dataContainer.appendChild(container)
                        })
                        dashboardDeletePostComment('post-delete')
                    } else if (helper(btn, 'Following') || helper(btn, 'Followers')) {
                        removeCurrentData();
                        obj = res.data
                        console.log(obj)
                        // console.log(socialURI)
                        let socialContainerOuter = document.createElement('div')
                        socialContainerOuter.classList.add('social-container-outer')
                        obj.forEach(data => {
                            let socialContainer = document.createElement('div')
                            socialContainer.classList.add('social-container')
                            let socialContainerImg = document.createElement('div')
                            socialContainerImg.classList.add('social-container-img')
                            let socialImg = document.createElement('img')
                            socialImg.alt = 'user-profile'
                            
                            socialImg.classList.add('d-author-profile-img')
                            socialImg.classList.add('i-author-profile')
                            socialImg.classList.add('mr-3')
                            let socialContainerUsername = document.createElement('div')
                            socialContainerUsername.classList.add('social-container-username')
                            let socialUsername = document.createElement('div')
                            socialUsername.classList.add('social-username')
                            socialUsername.textContent = data.fields.username
                            let socialFollowContainer = document.createElement('div')
                            socialFollowContainer.classList.add('social-follow-container')
                            let socialBtn = document.createElement('a')
                                socialBtn.href = `/follow/${data.fields.username}`
                            if(helper(btn, 'Followers')) {
                                if(data['additional fields'][1]) {
                                    socialImg.src = data['additional fields'][0]
                                    headerTitle.textContent = 'Followers'
                                    socialBtn.textContent = 'Followers'
                                    socialBtn.classList.add('file-btn')
                                } else {
                                    socialImg.src = data['additional fields'][0]
                                    socialBtn.textContent = 'Follow'
                                    
                                    socialBtn.classList.add('create')
                                }
                            } else {
                                headerTitle.textContent = 'Following'
                                socialImg.src = data['additional fields']
                                socialBtn.textContent = 'Following'
                                socialBtn.classList.add('file-btn')
                            }
                            socialBtn.classList.add('dashboard-custom-btn')
                            
                            socialContainer.appendChild(socialContainerImg)
                            socialContainerImg.appendChild(socialImg)
                            socialContainerImg.appendChild(socialContainerUsername)
                            socialContainerUsername.appendChild(socialUsername)
                            socialFollowContainer.appendChild(socialBtn)
                            socialContainer.appendChild(socialFollowContainer)
                            
                            socialContainerOuter.appendChild(socialContainer)
                            console.log(data.fields)
                            console.log(data['additional fields'])
                        })
                        dataContainer.appendChild(socialContainerOuter)

                        let dashBtns = document.querySelectorAll('.dashboard-custom-btn')

                        dashBtns.forEach(curr_btn => {
                            curr_btn.addEventListener('click', e => {
                                e.preventDefault()
                                let socParent = curr_btn.parentElement
                                let count = document.querySelector('.following-count')
                                let upperCount = document.querySelector('.main-following-count')
                                fetch(curr_btn.href)
                                .then(res => {
                                    if(curr_btn.textContent == 'Following') {
                                        socParent.parentElement.remove()
                                        count.textContent = parseInt(count.textContent) - 1
                                        upperCount.textContent = parseInt(upperCount.textContent) - 1
                                    } else {
                                        upperCount.textContent = parseInt(upperCount.textContent) + 1
                                        count.textContent = parseInt(count.textContent) + 1
                                        curr_btn.classList.remove('create')
                                        curr_btn.classList.add('file-btn')
                                        curr_btn.textContent = 'Following'
                                    }
                                })
                            })
                        })
                    } else if (helper(btn, 'Comment')) {
                        console.log(res.data)
                        obj = JSON.parse(res.data)
                        removeCurrentData();

                        obj.forEach(data => {
                            
                            const dashCommentContainer = document.createElement('div');
                            dashCommentContainer.classList.add('dash-comment-container');
                            const dashDescription = document.createElement('div');
                            dashDescription.classList.add('dash-description');
                            dashCommentContainer.appendChild(dashDescription);
                            const dashTitle = document.createElement('span');
                            dashTitle.classList.add('dash-title');
                            dashTitle.textContent = `${data.fields.comment.substring(0, 100)}...`;
                            const commentOn = document.createElement('span');
                            const anchorTitle = document.createElement('a');
                            // `/post/${slugify(data.fields.post)}`
                            anchorTitle.href = `/post/${slugify(data.fields.post)}`
                            anchorTitle.textContent = data.fields.post
                            commentOn.appendChild(anchorTitle);
                            let date = new Date(data.fields.created)
                            let month = date.toLocaleDateString();
                            let time = date.toLocaleTimeString();
                            const smallDate = document.createElement('small');
                            smallDate.classList.add('date');
                            smallDate.textContent = `${month} • ${time}`;
                            dashDescription.appendChild(dashTitle);
                            dashDescription.appendChild(commentOn);
                            dashDescription.appendChild(smallDate);
                            dataContainer.appendChild(dashCommentContainer);
                            const controls = document.createElement('div')
                            controls.classList.add('controls');
                            const idHidden = document.createElement('input');
                            idHidden.type = 'hidden'
                            idHidden.value = data.pk;
                            const deleteBtn = document.createElement('a')
                            deleteBtn.textContent = 'Delete'
                            deleteBtn.classList.add('comment-delete');
                            deleteBtn.classList.add('edit-delete');
                            controls.appendChild(idHidden)
                            // deleteBtn.href = `/api/comments/${data.pk}/delete/`
                            controls.appendChild(deleteBtn)
                            dashCommentContainer.appendChild(controls)
                        })
                        /* 
                        <div class="dash-comment-container">
                            <div class="dash-description">
                                <span class="dash-title ">Lorem ipsum dolor sit amet consectetur adipisicing elit... </span>
                                <span>commented on <a href=""> 4 things you should know</a></span>
                                <small class="date">
                                    Nov 12, 2020 • 12:48PM
                                </small>
                            </div>
                            <div class="controls">
                                <input type="hidden" id="id-edit" data-url="#">
                                <input type="hidden" id="id-delete" data-url="#">
                                <input type="hidden" id="id-post" data-url="#">
                                <a class="comment-delete delete" href="#">Delete</a>
                                <a class="comment-edit edit" href="#">Edit</a>
                            </div>
                        </div>
                        */
                       
                        // let deleteListener = document.querySelectorAll('.edit-delete')
                        
                        // deleteListener.forEach(btn => {
                        //     btn.addEventListener('click', () => {
                        //         alert('working')
                        //     })
                        // })

                        dashboardDeletePostComment('edit-delete')
                    }   
                })
                .catch(err => {
                    console.log(err)
                })
            })
        })
    }
}

dashboardDeletePostComment('post-delete')

dashboard();
follow();
popup();
searchToggle();
commentSec();
