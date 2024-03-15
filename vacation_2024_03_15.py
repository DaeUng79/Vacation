import streamlit as st
from datetime import datetime, timedelta

# 퇴직금 계산기 https://www.moel.go.kr/retirementpayCal.do

st.set_page_config(
    page_title="양산시 안식휴가 확인 서비스",
    page_icon="🍨",
) 

# 오늘의 날짜를 "0000년 00월 00일" 형식의 문자열로 변환
today_date = datetime.now()
formatted_today_date = today_date.strftime("%Y년 %m월 %d일")

# 두 날짜 사이의 일수를 계산
def calculate_days_between_dates(start_date_str, end_date_str, date_format="%Y%m%d"):
    try:
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        return (end_date - start_date).days+1
    except ValueError:
        return 0, "날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 다시 입력해주세요."



# 시작일로부터 주어진 일수 후의 기간을 계산하여 반환한다.
def calculate_period(appointment_date_str, total_days):
    
    try:
        appointment_date = datetime.strptime(appointment_date_str, "%Y%m%d")
        end_date = appointment_date + timedelta(days=total_days)
        
        years = end_date.year - appointment_date.year
        months = end_date.month - appointment_date.month
        days = end_date.day - appointment_date.day

        if months < 0:
            years -= 1
            months += 12
        if days < 0:
            months -= 1
            last_day_of_prev_month = (end_date.replace(day=1) - timedelta(days=1)).day
            days += last_day_of_prev_month
            if months < 0:
                years -= 1
                months += 12
                
        return years, months, days, ""
    except ValueError:
        return None, None, None, "날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 입력해주세요."
    

total_days = 0
육아휴직_합계 = 0
첫번째일수 = 0
두번째일수 = 0
###################################################################################################################
# 타이틀 작성 
st.markdown(
    "<style>.reportview-container .markdown-text-container { display:flex; justify-content: flex-end; }</style>"
    "<div class='caption' style='text-align: right;'> 개발 : 양산시 ChatGPT 학습동아리 팀</div>", 
    unsafe_allow_html=True)
st.title("양산시 안식휴가 확인 서비스 🍨")
st.subheader('', divider='rainbow')
txt = st.text_area(
    "",
    "1. 일자 입력으로 안식휴가를 확인할 수 있습니다.\n"
    "2. 재직기간별 최초 사용시 사용 3일 전까지 '행정과'에 복무사항으로 보고 하여야합니다.\n"
    "3. 차세대 인사랑시스템에 특별휴가 등록이 완료된 후 사용할 수 있습니다.\n"
    "4. 안식휴가는 소급 및 이월 사용이 불가합니다. ",height=120
    )

# 임용일자 입력 (YYYYMMDD 형식)
col1, col2 = st.columns([2.4,3])
with col1:
    appointment_date_str = st.text_input("◻️ 최초임용일", key="appointment", 
                                     placeholder="날짜는 20240315으로 입력 후 엔터")
with col2:    
    # 임용일자부터 현재까지의 근무일수 계산 및 표시
    if appointment_date_str:
        appointment_days = calculate_days_between_dates(appointment_date_str, datetime.now().strftime("%Y%m%d"))
        if appointment_days is not None:
            total_days += appointment_days
            st.markdown("")
            st.markdown("")
            st.write(f"🏆{formatted_today_date}까지 근무일수는 {appointment_days}일 입니다.")
        else:
            st.markdown("")
            st.markdown("")
            st.write("임용일자 형식이 올바르지 않습니다. YYYYMMDD 형식으로 다시 입력해주세요.")
st.caption("▪️ 차세대 인사랑시스템 '인사요약카드'에서 확인할 수 있습니다.")

# 군대 경력 입력 
col3, col4, col5 = st.columns([1.2,1.2,3])
with col3:
    military_service_start_date_str = st.text_input("◻️ 군대 입대일",placeholder="YYYYMMDD", key="military_start")
with col4:
    military_service_end_date_str = st.text_input("◻️ 군대 제대일",placeholder="YYYYMMDD", key="military_end")
with col5:
    # 군대 경력 기간 계산 및 표시
    if military_service_start_date_str and military_service_end_date_str:
        military_service_days = calculate_days_between_dates(military_service_start_date_str, military_service_end_date_str)
        if military_service_days is not None:
            total_days += military_service_days
            st.markdown("")
            st.markdown("")
            st.write(f"🔰군대 경력은 총 {military_service_days}일로 근무일수에 합산됩니다.")
        else:
            st.write("군대 경력 날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 다시 입력해주세요.")
st.caption("▪️ 차세대 인사랑시스템 '인사요약카드'에서 확인할 수 있습니다.")


# 질병 휴직 입력
col6, col7, col8 = st.columns([1.2,1.2,3])
with col6:
    sickness_start_date_str = st.text_input("◻️ 질병등 휴직 시작일",placeholder="YYYYMMDD", key="sickness_start")
with col7:
    sickness_end_date_str = st.text_input("◻️ 질병등 휴직 종료일",placeholder="YYYYMMDD", key="sickness_end")    
with col8:
# 질병 휴직 등 경력 기간 계산 및 표시
    if sickness_start_date_str and sickness_end_date_str:
        sickness_service_days = calculate_days_between_dates(sickness_start_date_str, sickness_end_date_str)
        if sickness_service_days is not None:
            total_days -= sickness_service_days
            st.markdown("")
            st.markdown("")
            st.markdown(f"🏣질병일수 {sickness_service_days}일은 경력에서 제외됩니다.")
        else:
            st.write("질병 등의 휴직 날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 다시 입력해주세요.")

#st.markdown("육아휴직 경력은 첫째 자녀만 입력하시면 됩니다.")
# 육아휴직 기간 입력
col9, col10, col11 = st.columns([1.2,1.2,3])
with col9:
    parental_leave_start_date_str = st.text_input("◻️첫째 육아휴직 시작일",placeholder="YYYYMMDD", key="parental_start")
with col10:
    parental_leave_end_date_str = st.text_input("◻️첫째 육아휴직 종료일",placeholder="YYYYMMDD", key="parental_end")
with col11:
    if parental_leave_start_date_str and parental_leave_end_date_str:
        첫번째일수 = calculate_days_between_dates(parental_leave_start_date_str,parental_leave_end_date_str)
        if 첫번째일수 is not None:
            st.markdown("")
            st.markdown("")
            st.write(f"🍭 첫 번째 육아휴직 기간은 {첫번째일수}일 입니다.")
        else:
            st.write("날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 다시 입력해주세요.")

# 추가 육아휴직 기간 입력
col12, col13, col14 = st.columns([1.2,1.2,3])
with col12:
    add_parental_leave_start_date_str = st.text_input("◻️첫째 추가 시작일",placeholder="YYYYMMDD", key="add_parental_start")
with col13:
    add_parental_leave_end_date_str = st.text_input("◻️첫째 추가 종료일",placeholder="YYYYMMDD", key="add_parental_end")
with col14:
# 육아휴직 기간 계산 및 표시
    if add_parental_leave_start_date_str and add_parental_leave_end_date_str:
        두번째일수 = calculate_days_between_dates(add_parental_leave_start_date_str,add_parental_leave_end_date_str)
        if 두번째일수 is not None:
            st.markdown("")
            st.write(f"🍭두 번째 육아휴직 기간은 {두번째일수}일 입니다.")
            st.write(f"👪육아휴직 총기간은 {첫번째일수 + 두번째일수}일 입니다.")
        else:
            st.write("날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 다시 입력해주세요.")

st.caption("▪️ 육아휴직자는 첫째 자녀에 한하여 최대 365일만 인정되며, 초과된 일수는 경력에서 제외됩니다.")
st.caption("▪️ 부모 모두 6개월 이상 휴직한 경우 행정과에 문의하시기 바랍니다.")    


if st.button("육아휴직 경력 확인"):
    합산결과 = 첫번째일수
    if 첫번째일수 and 두번째일수:
        합산결과 += 두번째일수

    if 합산결과 > 365:
        제외경력 = 합산결과 - 365
        total_days -= 제외경력
        st.write(f"첫째 자녀 육아휴직 경력기간은 최대 365일이므로, {제외경력}일은 경력에서 제외되었습니다.")
        st.write(f"확인된 경력인정 일수는 {total_days}일 입니다.")
    else:
        st.write(f"육아휴직 {합산결과}일 근무일수에 포함되어 있습니다.")
        st.write(f"경력인정 일수는 {total_days}일 입니다.")


# 계산 버튼
if st.button("재직기간 산정 및 안식휴가 조회"):
    years, months, days, error_message = calculate_period(appointment_date_str, total_days)
    
    if error_message:
        st.error(error_message)
    else:
        # 결과 출력
        st.write(f"산정된 경력일수는 {total_days}일이며, 재직기간은 {years}년 {months}월 {days}일 입니다.")

        # 안식휴가 대상 판단
        if years < 10:
            d_day = 3650 - total_days + 1 #다음날 소멸로 1 플러스
            future_date = today_date + timedelta(days=d_day)
            formatted_future_date = future_date.strftime("%Y년 %m월 %d일")
            st.subheader(f"🤐 안식휴가 대상이 아닙니다.")
            st.subheader(f"🏝️{formatted_future_date}부터 사용할수 있습니다.")
        elif 10 <= years < 20:
            d_day = 7300 - total_days + 1 
            future_date = today_date + timedelta(days=d_day)
            formatted_future_date = future_date.strftime("%Y년 %m월 %d일")         
            st.subheader(f"⛺ 1차 안식휴가 대상입니다.") 
            st.subheader(f"🤐 1차 안식휴가는 {formatted_future_date} 소멸됩니다.")
        elif 20 <= years < 30:
            d_day = 10950 - total_days + 1 
            future_date = today_date + timedelta(days=d_day)
            formatted_future_date = future_date.strftime("%Y년 %m월 %d일")         
            st.subheader(f"🏝️ 1차 안식휴가 종료 및 2차 안식휴가 사용가능합니다.")
            st.subheader(f"🤐 2차 안식휴가는 {formatted_future_date} 소멸됩니다.")
        else:  # 30년 이상
            st.subheader("🤐 1차, 2차 안식휴가는 종료 되었습니다.")
            st.subheader("👨‍👨‍👧‍👧 3차 안식휴가를 사용 할 수 있습니다.")