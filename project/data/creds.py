# These credentials will be used to authenticate you into the MyTUD/OSIRIS
net_id: str = ""
password: str = ""

# Ignore this part
COURSE_URL = "https://my.tudelft.nl/#/inschrijven/cursus/:id"
COURSE_SEARCH = '/html/body/ion-app/app-root/ion-app-wrapper/ion-split-pane/ion-nav/page-enroll-course/enroll-base-component/osi-page-left/ \
                 ion-content/div[2]/div/osi-enroll-course-flow/div/div/osi-course-enroll-search/osi-elastic-search/ion-row/ion-col[2]/div/div/ \
                 div[1]/div[2]/div/ion-searchbar/div/input'