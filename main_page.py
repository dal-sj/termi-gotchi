import streamlit as st
from gotchi import Egg

st.title("Termi-Gotchi")

if 'pet' not in st.session_state:
    st.session_state.pet = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

if st.session_state.pet is None:
    st.header("새로운 터미고치에게 이름을 지어주세요!")
    
    pet_name = st.text_input("펫의 이름:")
    pet_species = st.radio(
        "펫의 종류를 선택하세요:",
        ('default', 'bear'),
        format_func=lambda x: '토끼' if x == 'default' else '곰')


    if st.button("이 이름으로 시작하기"):
        if pet_name:
            st.session_state.pet = Egg(name=pet_name, species=pet_species)
            st.session_state.messages.append(f"{pet_name} 알이 생겼습니다!")
            st.rerun()
        else:
            st.warning("펫의 이름을 입력해야 합니다.")

else:
    pet = st.session_state.pet

    
    main_col1, main_col2 = st.columns([2, 1])

    
    with main_col1:
        st.code('\n'.join(pet.get_art()), language='text')
        st.divider()
        st.write("**로그**")
        
        message_container = st.container(height=200, border=True)
        for message in st.session_state.messages:
            message_container.text(message)
        st.session_state.messages = []

    
    with main_col2:
        st.markdown(f"**이름**: {pet.name}")
        st.markdown(f"**성장 단계**: {pet.get_stage()}")
        st.markdown(f"**나이**: {pet.age}")
        st.markdown(f"**종류**: {'토끼' if pet.species == 'default' else '곰'}")
        
        st.progress(pet.satiety * 10, text=f"**포만감**: {pet.satiety}/10")
        st.progress(pet.happiness * 10, text=f"**행복도**: {pet.happiness}/10")
        
        st.divider()

        
        def handle_action(messages, new_pet_state):
            if messages:
                st.session_state.messages.extend(messages)
            if new_pet_state is not pet:
                st.session_state.messages.append(f"✨ {pet.name}이(가) {new_pet_state.get_stage()}(으)로 진화했다! ✨")
                st.session_state.pet = new_pet_state
            st.rerun()

        
        if not pet.is_dead:
            commands = pet.get_commands()
            
            if len(commands) > 2:
                btn_cols = st.columns(2)
                for i, command_text in enumerate(commands):
                    with btn_cols[i % 2]:
                        if st.button(command_text, key=f"cmd_{i}", use_container_width=True):
                            action_messages = pet.handle_input(command_text)
                            new_pet, update_messages = pet.update()
                            handle_action(action_messages + update_messages, new_pet)
            else: 
                for i, command_text in enumerate(commands):
                    if st.button(command_text, key=f"cmd_{i}", use_container_width=True):
                        action_messages = pet.handle_input(command_text)
                        new_pet, update_messages = pet.update()
                        handle_action(action_messages + update_messages, new_pet)

            if st.button("시간 보내기", use_container_width=True):
                new_pet, update_messages = pet.update()
                handle_action(update_messages, new_pet)
        
        
        else:
            st.error(f"{pet.name}은(는) 더 이상 존재하지 않습니다. 새로운 펫을 키우려면 '처음으로 돌아가기' 버튼을 누르세요.")
        
        st.divider()

        
        if st.button("처음으로 돌아가기", type="secondary", use_container_width=True, key="reset_game"):
            st.session_state.pet = None
            st.session_state.messages = []
            st.rerun()