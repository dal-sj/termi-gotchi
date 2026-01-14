import random
from art import ART_DATA

class Pet:
    def __init__(self, name="Gotchi", species="default", satiety=5, happiness=5, age=0, sickness=0):
        self.name = name
        self.species = species
        
        self.satiety = satiety
        self.happiness = happiness
        self.age = age
        self.sickness = sickness
        self.is_dirty = False
        self.is_dead = False
        self.training_count = 0
        
        self.sub_state = 'default'
        self.evolving = False

    def update(self):
        messages = []

        
        if self.sickness >= 10:
            self.is_dead = True
            return self, [f"{self.name}이(가) 병을 이기지 못하고 쓰러졌습니다... 별이 되었습니다."]
        if self.satiety <= 0 and self.happiness <= 0:
            self.is_dead = True
            return self, [f"{self.name}이(가) 기력과 행복을 모두 잃고... 별이 되었습니다."]
        
        self.age += 1

        if self.is_dirty:
            self.happiness = max(0, self.happiness - 1)
            self.sickness = min(10, self.sickness + 1)
            messages.append(f"주변이 더러워 {self.name}의 기분이 안 좋아 보입니다.")

        if self.satiety <= 1 or self.happiness <= 1:
            self.sickness = min(10, self.sickness + 1)
        elif self.satiety >= 8 and self.happiness >= 8 and self.sickness > 0:
            self.sickness = max(0, self.sickness - 1)

        if self.satiety > 0:
            self.satiety -= 1
        if self.happiness > 0:
            self.happiness -= 1

        previous_sub_state = self.sub_state 

        if self.sickness > 5:
            self.sub_state = 'sick'
        elif self.satiety < 3:
            self.sub_state = 'hungry'
        elif self.happiness > 7:
            self.sub_state = 'happy'
        else:
            self.sub_state = 'default'
        
        
        if self.sub_state != previous_sub_state:
            if self.sub_state == 'sick':
                messages.append(f"😥 {self.name}이(가) 아파 보입니다. 약이 필요할 것 같아요.")
            elif self.sub_state == 'hungry':
                messages.append(f"🍽️ {self.name}의 배에서 꼬르륵 소리가 납니다. 배가 고픈가 봐요.")
            elif self.sub_state == 'happy':
                messages.append(f"😊 {self.name}이(가) 행복해 보입니다! 기분 좋은 하루예요.")
            elif self.sub_state == 'default':
                messages.append(f"😌 {self.name}이(가) 이제 안정된 것 같습니다.")
        
        return self, messages
    
    def get_stage(self):
        match self.__class__.__name__:
            case 'Egg':
                return "알"
            case 'Infant':
                return '유아기'
            case 'Child':
                return '유년기'
            case 'Adolescent':
                return '청소년기'
            case 'Adult':
                return '성년기'
    
    def get_art(self):
        stage_name = self.__class__.__name__
        stage_art_data = ART_DATA[self.species].get(stage_name)

        # 우선순위: dead > sick > dirty > other sub_states
        if self.is_dead:
            art = stage_art_data.get('dead')
            if art:
                return art

        if self.sub_state == 'sick':
            art = stage_art_data.get('sick')
            if art:
                return art

        if self.is_dirty:
            art = stage_art_data.get('dirty')
            if art:
                return art

        return stage_art_data.get(self.sub_state, stage_art_data.get('default'))

    def feed(self, action_messages=None):
        self.satiety = min(10, self.satiety + 5)
        self.happiness = min(10, self.happiness + 1)
        
        if action_messages is None:
            action_messages = [
                f"{self.name}이(가) 허겁지겁 밥을 먹습니다. 아주 배가 고팠나봅니다.",
                f"맛있는 식사에 {self.name}이(가) 만족한 듯 보입니다.",
                f"{self.name}이(가) 그릇에 얼굴을 파묻고 정신없이 먹고 있습니다."
            ]
        
        final_messages = [random.choice(action_messages)]
        
        if random.random() < 0.4:
            self.is_dirty = True
            final_messages.append(f"식사를 마친 {self.name}의 주변이 더러워졌습니다.")

        return final_messages

    def play(self, action_messages=None):
        self.happiness = min(10, self.happiness + 3)
        
        if action_messages is None:
            action_messages = [
                f"{self.name}이(가) 신나게 제자리를 빙글빙글 돕니다.",
                f"당신과 함께 즐거운 시간을 보내며 {self.name}의 기분이 좋아 보입니다.",
                f"장난감을 가지고 놀며 {self.name}이(가) 행복해합니다."
            ]
        return [random.choice(action_messages)]

    def train(self, success_rate=1.0):
        if random.random() < success_rate:
            self.training_count += 1
            self.happiness = min(10, self.happiness + 1)
            return [f"{self.name}이(가) 훈련을 성공적으로 마쳤습니다! (현재 훈련 횟수: {self.training_count})"]
        else:
            self.happiness = max(0, self.happiness - 1)
            return [f"{self.name}이(가) 훈련에 집중하지 못했습니다..."]

    def walk(self):
        self.happiness = min(10, self.happiness + 4)
        action_messages = [
            f"상쾌한 공기를 마시며 {self.name}이(가) 즐겁게 산책합니다.",
            f"산책 중 {self.name}이(가) 신기한 것을 발견하고 킁킁거립니다.",
        ]
        return [random.choice(action_messages)]

    def spend_time(self):
        self.happiness = min(10, self.happiness + 2)
        action_messages = [
            f"{self.name}이(가) 당신의 곁에 조용히 앉아 시간을 보냅니다.",
            f"함께 창 밖을 바라봅니다. 평화로운 시간입니다.",
        ]
        return [random.choice(action_messages)]

    def medicate(self):
        self.sickness = max(0, self.sickness - 5)
        self.happiness = max(0, self.happiness - 2)
        action_messages = [ f"쓴 약을 먹고 {self.name}이(가) 몸을 부르르 떱니다." ]
        return [random.choice(action_messages)]

    def clean(self):
        if self.is_dirty:
            self.is_dirty = False
            self.happiness = min(10, self.happiness + 1)
            return [f"주변이 깨끗해져서 {self.name}의 기분이 좋아 보입니다."]
        return ["치울 것이 없습니다. 주변은 이미 깨끗합니다."]

    def get_commands(self):
        if self.is_dead:
            return []
        
        commands = []
        if self.is_dirty:
            commands.append('치우기')
        if self.sub_state == 'sick':
            commands.append('약먹이기')
        return commands

class Egg(Pet):
    def get_commands(self):
        return ['온도 높이기', '쓰다듬기']

    def __init__(self, name="Gotchi", species="default", satiety=5, happiness=5, age=0, sickness=0):
        super().__init__(name, species, satiety, happiness, age, 0)
        self.is_dirty = False

    def handle_input(self, command):
        if command == "온도 높이기": return self.feed()
        elif command == "쓰다듬기": return self.play()
        else: return ["반응이 없습니다."]

    def feed(self):
        self.satiety = min(10, self.satiety + 5)
        self.happiness = min(10, self.happiness + 1)
        return ["알의 온도가 올라가며 조금 더 따뜻해졌습니다."]

    def play(self):
        self.happiness = min(10, self.happiness + 2)
        self.training_count += 1
        return ["조심스럽게 알을 쓰다듬자, 온기가 느껴지는 것 같습니다. (훈련 횟수: {})".format(self.training_count)]

    def update(self):
        pet, messages = super().update()
        if not self.evolving and self.age > 3 and self.happiness > 7 and self.training_count >= 5:
            self.evolving = True
            messages.append("알에 작은 금이 가기 시작했습니다!")
        if self.evolving:
            messages.append("껍질이 부서지며... 작은 아이가 태어났습니다!")
            return Infant(name=self.name, species=self.species, satiety=self.satiety, happiness=self.happiness, age=self.age, sickness=self.sickness), messages
        return pet, messages

class Infant(Pet):
    def get_commands(self):
        base_commands = ['이유식 먹이기', '딸랑이 흔들기', '뒤집기 연습']
        return base_commands + super().get_commands()
    
    def handle_input(self, command):
        if command == "이유식 먹이기": return self.feed()
        elif command == "딸랑이 흔들기": return self.play()
        elif command == "뒤집기 연습": return self.train()
        elif command == "약먹이기": return self.medicate()
        elif command == "치우기": return self.clean()
        else: return ["알아들을 수 없는 말입니다."]

    def train(self):
        return super().train(success_rate=0.8)

    def update(self):
        pet, messages = super().update()
        if not self.evolving and self.age > 8 and self.satiety > 5 and self.happiness > 5 and self.training_count >= 5:
            self.evolving = True
            messages.append(f"{self.name}의 몸이 희미한 빛에 휩싸입니다...!")
        if self.evolving:
            messages.append("빛이 강해지며 몸의 형태가 변하기 시작합니다!")
            return Child(name=self.name, species=self.species, satiety=self.satiety, happiness=self.happiness, age=self.age, sickness=self.sickness), messages
        return pet, messages

class Child(Pet):
    def get_commands(self):
        base_commands = ['밥주기', '놀아주기', '훈련하기']
        return base_commands + super().get_commands()

    def handle_input(self, command):
        if command == "밥주기": return self.feed()
        elif command == "놀아주기": return self.play()
        elif command == "훈련하기": return self.train()
        elif command == "약먹이기": return self.medicate()
        elif command == "치우기": return self.clean()
        else: return ["알아들을 수 없는 말입니다."]

    def train(self):
        return super().train(success_rate=0.7)

    def update(self):
        pet, messages = super().update()
        if not self.evolving and self.age > 18 and self.satiety > 7 and self.happiness > 7 and self.training_count >= 5:
            self.evolving = True
            messages.append(f"{self.name}의 몸이 부르르 떨리며 빛나기 시작합니다...!")
        if self.evolving:
            messages.append("한층 더 자란 모습으로 변했습니다!")
            return Adolescent(name=self.name, species=self.species, satiety=self.satiety, happiness=self.happiness, age=self.age, sickness=self.sickness), messages
        return pet, messages

class Adolescent(Pet):
    def get_commands(self):
        base_commands = ['밥주기', '산책하기', '고급 훈련']
        return base_commands + super().get_commands()

    def handle_input(self, command):
        if command == "밥주기": return self.feed()
        elif command == "산책하기": return self.walk()
        elif command == "고급 훈련": return self.train()
        elif command == "약먹이기": return self.medicate()
        elif command == "치우기": return self.clean()
        else: return ["알아들을 수 없는 말입니다."]

    def train(self):
        return super().train(success_rate=0.6)

    def update(self):
        pet, messages = super().update()
        if not self.evolving and self.age > 35 and self.satiety > 8 and self.happiness > 8 and self.training_count >= 5:
            self.evolving = True
            messages.append("성장의 마지막 단계에 다다른 것 같습니다...!")
        if self.evolving:
            messages.append(f"눈부신 빛과 함께... {self.name}이(가) 마침내 최종 모습으로 진화했습니다!")
            return Adult(name=self.name, species=self.species, satiety=self.satiety, happiness=self.happiness, age=self.age, sickness=self.sickness), messages
        return pet, messages

class Adult(Pet):
    def get_commands(self):
        base_commands = ['식사하기', '함께 시간보내기']
        return base_commands + super().get_commands()

    def handle_input(self, command):
        if command == "식사하기": return self.feed()
        elif command == "함께 시간보내기": return self.spend_time()
        elif command == "약먹이기": return self.medicate()
        elif command == "치우기": return self.clean()
        else: return ["알아들을 수 없는 말입니다."]
    
    def update(self):
        return super().update()
