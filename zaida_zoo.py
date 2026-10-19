class Animal:
    def __init__(self, name, species, age, weight, diet_type):
        # 5 poley
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.diet_type = diet_type

    def make_sound(self):
        return self.name + " издаёт характерный звук!"

    def get_info(self):
        return "Кличка: " + str(self.name) + " | Вид: " + str(self.species) + " | Возраст: " + str(
            self.age) + " лет | Вес: " + str(self.weight) + " кг | Питание: " + str(self.diet_type)


class Reptile(Animal):
    def __init__(self, name, species, age, weight, diet_type, scale_type, is_venomous):
        super().__init__(name, species, age, weight, diet_type)
        self.scale_type = scale_type
        self.is_venomous = is_venomous

    def bask_in_sun(self):
        return self.name + " неподвижно греется на теплом камне."

    def perform_trick(self):
        return '🐍 "ШОУ КОБР И ПИТОНОВ" — ' + self.name + ' танцует под звуки флейты и пролезает через горящее кольцо!'


class Amphibian(Animal):
    def __init__(self, name, species, age, weight, diet_type, skin_humidity, metamorphosis_stage):
        super().__init__(name, species, age, weight, diet_type)
        self.skin_humidity = skin_humidity
        self.metamorphosis_stage = metamorphosis_stage

    def breathe_through_skin(self):
        return self.name + " дышит через влажную кожу под водой."

    def perform_trick(self):
        return '🐸 "ШОУ ЛЯГУШЕК-АКРОБАТОВ" — ' + self.name + ' делает тройное сальто над бассейном и ловко ловит кувшинку в воздухе!'


class ZooShow:
    def __init__(self, reptile_star, amphibian_star):
        self.reptile_star = reptile_star
        self.amphibian_star = amphibian_star

    def start_show(self):
        print("============================================================")
        print("🎪 ДОБРО ПОЖАЛОВАТЬ В НАШ ЗООПАРК-ТЕАТР! 🎪")
        print("============================================================")

        print("\nКакое шоу вы хотите посетить?")
        print("1. Шоу Пресмыкающихся")
        print("2. Шоу Земноводных")

        while True:
            vibor_shou = input("Введите номер (1 или 2): ").strip()
            if vibor_shou == "1" or vibor_shou == "2":
                break
            else:
                print("Ошибка! Введите 1 или 2:")

        print("\nДоступные варианты билетов:")
        print("  [1] Обычное место (сектор Б) — 500 руб.")
        print("  [2] VIP-место (первый ряд + подарок) — 1200 руб.")

        while True:
            vibor_bileta = input("Выберите тип билета (1 или 2): ").strip()
            if vibor_bileta == "1" or vibor_bileta == "2":
                break
            else:
                print("Ошибка! Введите 1 или 2:")

        if vibor_bileta == "1":
            bilet_name = "Обычное место (сектор Б)"
            cena = 500
        else:
            bilet_name = "VIP-место (первый ряд + подарок)"
            cena = 1200

        print("\n--------------------------------------------------")
        print("🎟️  ВАШ БИЛЕТ УСПЕШНО ОФОРМЛЕН!")
        print("• Категория: " + bilet_name)
        print("• К оплате: " + str(cena) + " рублей")
        print("--------------------------------------------------")

        print("\n🎉 НАЧАЛО ПРЕДСТАВЛЕНИЯ!\n")

        if vibor_shou == "1":
            print(self.reptile_star.perform_trick())
        elif vibor_shou == "2":
            print(self.amphibian_star.perform_trick())

        print("\nПриятного просмотра!")


if __name__ == "__main__":
    cobra = Reptile("Нагайна", "Королевская кобра", 5, 6.5, "Хищник", "Гладкая чешуя", True)
    frog = Amphibian("Квакша", "Древесная лягушка", 2, 0.3, "Насекомоядное", "Влажная", "Взрослая особь")

    show = ZooShow(cobra, frog)
    show.start_show()
