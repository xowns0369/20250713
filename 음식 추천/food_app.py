import streamlit as st
import pandas as pd
import random

def load_food_data():
    """음식 데이터를 로드합니다."""
    food_data = {}
    try:
        with open('음식 목록.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        for line in lines[2:]:  # 첫 두 줄은 건너뛰기
            if ':' in line:
                food_name, attributes = line.strip().split(':', 1)
                food_name = food_name.strip()
                attributes = [attr.strip() for attr in attributes.split(',')]
                food_data[food_name] = attributes
                
    except FileNotFoundError:
        # 파일이 없으면 기본 데이터 사용
        food_data = {
            "김치찌개": ["점심", "저녁", "아침", "국물있음", "매움", "안매움", "혼자", "여럿이"],
            "된장찌개": ["아침", "점심", "저녁", "국물있음", "안매움", "혼자", "여럿이"],
            "불고기": ["아침", "점심", "국물없음", "혼자", "여럿이", "안매움"],
            "라면": ["아침", "점심", "저녁", "간식", "야식", "혼자", "여럿이", "매움", "안매움", "국물있음"],
            "피자": ["점심", "간식", "야식", "국물없음", "안매움", "여럿이"],
            "치킨": ["저녁", "야식", "국물없음", "안매움", "여럿이"],
            "샐러드": ["아침", "점심", "간식", "국물없음", "혼자", "안매움", "다이어트"],
            "김밥": ["아침", "점심", "간식", "국물없음", "안매움", "혼자", "다이어트"]
        }
        
    return food_data

def find_matching_foods(food_data, selected_attrs):
    """선택된 속성과 일치하는 음식들을 찾습니다."""
    matching_foods = []
    
    for food_name, food_attrs in food_data.items():
        # 선택된 속성 중 하나라도 음식의 속성에 포함되어 있으면 매칭
        if any(attr in food_attrs for attr in selected_attrs):
            # 매칭 점수 계산 (일치하는 속성 수)
            match_score = sum(1 for attr in selected_attrs if attr in food_attrs)
            matching_foods.append({
                '음식명': food_name,
                '매칭점수': match_score,
                '총점수': len(selected_attrs),
                '일치율': round(match_score / len(selected_attrs) * 100, 1),
                '속성': ', '.join(food_attrs)
            })
    
    # 매칭 점수로 정렬 (높은 순)
    matching_foods.sort(key=lambda x: x['매칭점수'], reverse=True)
    return matching_foods

def main():
    st.set_page_config(
        page_title="🍽️ 음식 추천 시스템",
        page_icon="🍽️",
        layout="wide"
    )
    
    # 제목
    st.title("🍽️ 음식 추천 시스템")
    st.markdown("원하는 속성을 선택하면 그에 맞는 음식을 추천해드립니다!")
    
    # 음식 데이터 로드
    food_data = load_food_data()
    
    # 사이드바에 속성 선택
    st.sidebar.header("📋 원하는 속성을 선택하세요")
    
    # 속성들을 카테고리별로 분류
    meal_categories = {
        "🍽️ 식사 시간": ["아침", "점심", "저녁", "간식", "야식"],
        "👥 상황": ["혼자", "여럿이", "회식"],
        "🌶️ 맛": ["매움", "안매움"],
        "🍲 국물": ["국물있음", "국물없음"],
        "💪 기타": ["다이어트","데이트","집", "회사", "외식", "배달", "야외"]
    }
    
    selected_attributes = []
    
    for category, attrs in meal_categories.items():
        st.sidebar.subheader(category)
        for attr in attrs:
            if st.sidebar.checkbox(attr, key=attr):
                selected_attributes.append(attr)
    
    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 추천 결과")
        
        if not selected_attributes:
            st.info("👈 왼쪽 사이드바에서 원하는 속성을 선택해주세요!(중복가능!)")
            
            # 랜덤 추천 버튼
            if st.button("🎲 랜덤 추천 받기"):
                food_name = random.choice(list(food_data.keys()))
                food_attrs = food_data[food_name]
                
                st.success(f"🎲 랜덤 추천 결과")
                st.write(f"**추천 음식:** {food_name}")
                st.write(f"**속성:** {', '.join(food_attrs)}")
                st.balloons()
        else:
            st.write(f"**선택하신 속성:** {', '.join(selected_attributes)}")
            
            matching_foods = find_matching_foods(food_data, selected_attributes)
            
            if not matching_foods:
                st.warning("선택하신 속성과 일치하는 음식이 없습니다. 다른 속성을 선택해보세요!")
            else:
                st.success(f"총 {len(matching_foods)}개의 음식이 추천됩니다!")
                
                # 상위 10개 음식을 표 형태로 표시
                df = pd.DataFrame(matching_foods[:10])
                
                # 점수에 따른 색상 적용
                def color_score(val):
                    if val >= 80:
                        return 'background-color: #90EE90'  # 연한 초록
                    elif val >= 60:
                        return 'background-color: #FFE4B5'  # 연한 주황
                    else:
                        return 'background-color: #FFB6C1'  # 연한 빨강
                
                styled_df = df.style.applymap(color_score, subset=['일치율'])
                st.dataframe(styled_df, use_container_width=True)
                
                if len(matching_foods) > 10:
                    st.info(f"... 외 {len(matching_foods) - 10}개 더 있습니다.")
    
    with col2:
        st.header("📊 통계")
        
        if selected_attributes:
            matching_foods = find_matching_foods(food_data, selected_attributes)
            
            if matching_foods:
                # 통계 정보
                st.metric("추천 음식 수", len(matching_foods))
                
                if matching_foods:
                    avg_score = sum(food['일치율'] for food in matching_foods) / len(matching_foods)
                    st.metric("평균 일치율", f"{avg_score:.1f}%")
                    
                    max_score = max(food['일치율'] for food in matching_foods)
                    st.metric("최고 일치율", f"{max_score}%")
                
                # 일치율 분포
                st.subheader("일치율 분포")
                score_ranges = {
                    "90% 이상": len([f for f in matching_foods if f['일치율'] >= 90]),
                    "70-89%": len([f for f in matching_foods if 70 <= f['일치율'] < 90]),
                    "50-69%": len([f for f in matching_foods if 50 <= f['일치율'] < 70]),
                    "50% 미만": len([f for f in matching_foods if f['일치율'] < 50])
                }
                
                for range_name, count in score_ranges.items():
                    if count > 0:
                        st.write(f"{range_name}: {count}개")
    
    # 하단에 추가 정보
    st.markdown("---")
    st.markdown("### 💡 사용 팁")
    st.markdown("""
    - **더 정확한 추천을 위해**: 여러 속성을 선택하면 더 맞춤형 추천을 받을 수 있습니다
    - **일치율**: 선택한 속성 중 몇 %가 해당 음식과 일치하는지 나타냅니다
    - **랜덤 추천**: 고민할 시간이 없다면 랜덤 추천을 사용해보세요!
    """)
    
    # 음식 데이터 정보
    with st.expander("📋 전체 음식 목록 보기"):
        food_df = pd.DataFrame([
            {'음식명': name, '속성': ', '.join(attrs)} 
            for name, attrs in food_data.items()
        ])
        st.dataframe(food_df, use_container_width=True)

if __name__ == "__main__":
    main()
