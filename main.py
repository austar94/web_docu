from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class WebControll:
    def __init__(self):
        # options = webdriver.ChromeOptions()
        #
        # # headless 옵션 설정
        # # options.add_argument('headless')
        # # options.add_argument("no-sandbox")
        #
        # # 브라우저 윈도우 사이즈
        # options.add_argument('window-size=1920x1080')
        #
        # # 사람처럼 보이게 하는 옵션들
        # options.add_argument("disable-gpu")  # 가속 사용 x
        # options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
        # options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

        # chrome 웹 드라이버 생성
        # self.driver = webdriver.Chrome('C:\project\python\docu\chromedriver.exe', chrome_options=options)
        self.driver = webdriver.Chrome('C:\project\python\docu\chromedriver.exe')   # 81버전
        self.mainPage = ""  # 메인화면 핸들값

        self.targetOrg = "경기도 시립중앙도서관"  # 목표하는 기관 명
        self.userID = "fosdk@lsdi.com"
        self.userPWD = "vidhsok23"
        self.userType = 1   # 1: 개인 사용자 , 2: 법인, 단체 사용자


        self.main_title = "문서24"  # 메인화면 타이틀
        self.main_documentClassName = "mv_action.menu1"  # 메인화면 문서작성 메뉴 class 명

        self.login_title = "로그인 - 문서24" # 로그인페이지 타이틀
        self.login_tabXpath = "//div[@class=\"link_menu\"]/ul[@class=\"lm_type1\"]/li[" + str(self.userType) + "]"  # 로그인화면 유형선택 탭 class 명
        self.login_idInputId = "id" # 로그인 페이지 아이디 입력 아이디
        self.login_pwdInputId = "password"  # 로그인 페이지 비밀번호 입력 아이디
        self.login_loginBtnClassName = "loginBtn"   # 로그인 페이지 로그인 버튼

        self.write_title = "문서 작성 - 문서24"   # 문서 작성 페이지 타이틀
        self.write_chkAllClassName = "all_check"  # 문서작성 페이지 제출전 동의 사항 전체동의 버튼 아이디
        self.write_orgPopupId = "ldapSearch"    # 반는기관 검색 팝업 호출 버튼 아이write_orgSearchTextId디
        self.write_orgSearchTextId = "searchOrgNm"  # 받는기관 검색 입력창 아이디
        self.write_orgSearchBtn = "//form[@id=\"Form\"]/button"    # 받는기관 검색 버튼

    def run(self):
        try:
            # url 로딩
            self.driver.get("https://open.gdoc.go.kr/index.do")
            self.mainPage = self.driver.window_handles[0]  # 메인 이외의 페이지 삭제를 위해 메인페이지 값 저장
            
            # 메인 화면에서 글쓰기 화면으로 이동
            self.move_to_writePage()
            
            # 해당 사이트가 문서사이트가 맞는지 확인
            # assert 구문은 뒤의 조건이 True 가 아닐경우 AssertError 를 발생시킴
            assert self.main_title in self.driver.title

            # 이동된 곳이 로그인사이트일경우 로그인 동작 실행
            if self.driver.title == self.login_title:
                self.pageLogin()

            # 로그인 후 문서작성 페이지로 이동했는지 확인
            if self.driver.title == self.write_title:
                # 문서 작성
                self.write_doc()
            else:
                print(self.driver.title)
                print(self.write_title)
                raise Exception("예상치 못한 페이지로 이동되었습니다. 재 정의가 필요합니다.")

            print("문서24 사이트 접속 완료")
        except Exception as e:
            print('예외가 발생했습니다.', e)
            # self.driver.close()

    # 문서 작성
    def write_doc(self):
        time.sleep(1)

        # 제출 전 동의 사항 전체동의
        self.driver.find_element_by_class_name(self.write_chkAllClassName).click()

        # 내용 입력 전 경고팝업 닫기
        self.driver.find_element_by_xpath("//div[@class=\"jconfirm-buttons\"]/button").click()

        # 문서받는 기관 검색 팝업 띄우기jconfirm-buttons
        self.driver.find_element_by_id(self.write_orgPopupId).click()

        # 팝업 생성 후 잠시 대기
        time.sleep(3)

        # 기본검색 조직 입력
        self.driver.find_element_by_id(self.write_orgSearchTextId).send_keys(self.targetOrg)

        # 검색버튼 클릭
        self.driver.find_element_by_xpath(self.write_orgSearchBtn).click()


    #메인페이지에서 문서작성 페이지로 이동
    def move_to_writePage(self):
        # mainPage 이외의 다른 window 가 존재할 경우 close 시킴
        self.close_sidePage()

        self.driver.switch_to.window(self.mainPage)  # 메인 페이지로 스위칭

        # 문서작성 클릭
        self.driver.find_element_by_class_name(self.main_documentClassName).click()

    # 로그인 동작
    def pageLogin(self):
        print("로그인 동작 작동")

        # 사용자 유형에 맞게 탭 선택
        self.driver.find_element_by_xpath(self.login_tabXpath).click()

        # 아이디, 비밀번호 입력
        self.driver.find_element_by_id(self.login_idInputId).send_keys(self.userID)
        self.driver.find_element_by_id(self.login_pwdInputId).send_keys(self.userPWD)

        # 로그인 버튼
        self.driver.find_element_by_class_name(self.login_loginBtnClassName).click()

        time.sleep(1)

    # mainPage 이외의 다른 window 가 존재할 경우 close 시킴
    def close_sidePage(self):
        print("mainPage 이외의 sidePage 종료")
        for handle in self.driver.window_handles:

            # 메인페이지를 제외한 나머지 페이지 종료
            if handle == self.mainPage:
                continue

            self.driver.switch_to.window(handle)  # 서브 페이지로 스위칭
            self.driver.close()  # 스위칭된 페이지 종료



web = WebControll()
web.run()