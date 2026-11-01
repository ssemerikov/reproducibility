# Curriculum expert survey (36 respondents, 20 August to 13 September 2021)

Online questionnaire (Google Forms) "Зміст навчання основ квантової інформатики учнів ліцеїв" ("Content of teaching the fundamentals of quantum informatics to lyceum students"), the export of which is titled "Квантову інформатику - в школу!". The form is reproduced in Lehka (2021), Appendix B (Додаток Б), printed pp. 203-218, https://doi.org/10.31812/123456789/7042. The rated-item wording below is taken from the column headers of the original export, which is authoritative; it differs from the thesis reproduction in two places (item 1.01 is abbreviated there, and item 5.04 reads "дикогерентності" for "декогерентності"). English renderings are drafted with AI assistance and await verification by L. V. Lehka; the Ukrainian text is the evidence.

## Invitation (verbatim)

> Шановні колеги!
>
> З метою добору змісту навчання факультативного курсу "Основи квантової інформатики" для учнів 10-11 класів просимо Вас оцінити значущість складових Європейської рамки компетенцій у галузі квантових технологій (https://qt.eu/app/uploads/2019/02/Competence_Framework_for_QT_1.0_May2021.pdf) та надати Ваші рекомендації щодо змісту навчання шкільного курсу основ квантової інформатики.

*English:* Dear colleagues! To select the content of the elective course "Fundamentals of quantum informatics" for grades 10-11, we ask you to rate the significance of the components of the European Competence Framework for Quantum Technologies (CFQT v1.0) and to give your recommendations on the content of a school course on the fundamentals of quantum informatics.

## Response scale for the 64 rated items

| Label (verbatim) | English | Code used for the thesis score |
|---|---|---|
| зовсім не важливо | not important at all | -1 |
| мало важливо | slightly important | 1 |
| утруднююсь відповісти | unable to answer | 0 |
| скоріше, важливо | rather important | 2 |
| дуже важливо | very important | 3 |

The export also contains the label "скоріше важливо" (without the comma) in 63 responses to items 2.01-2.04. The workbook formula did not match it and stored code 3; the raw-label recoding treats it as code 2. Both codes are released (`raw_label_code`, `stored_code` in `curriculum_responses_coded.csv`). The thesis weighted score of an item is the sum over respondents of code x self-rated competence weight (see `CODEBOOK.md`).

Each domain block below lists the instructions, the descriptor text shown to respondents (Ukrainian rendering of CFQT v1.0; English original: Greinert and Müller, 2021, *Competence Framework for Quantum Technologies*, version 1.0), the rated items and the open question. Rated items are released in `curriculum_responses_deidentified.csv` as column `item_<id>`.

## Domain 1: Фізичні основи квантових технологій (Physical foundations)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з фізичних основ квантових технологій:**  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain.

- основні поняття квантової фізики (оптики, механіки): суперпозиція, інтерференція; квантування енергії, пов’язані (заплутані) стани, тунелювання; статистична природа квантової фізики; принцип невизначеності Гейзенберга; прості приклади декогеренції (релаксація, дефазування, втрата фотонів); нерівності Белла, стани Белла, квантова телепортація, надщільне кодування; фотонні взаємодії атомів і матерії; поляризаційні ступені свободи (сфера Пуанкаре);
- динаміка кубітів: поняття кубіту, сфера Блоха, маніпулювання кубітами за допомогою імпульсів, математичний опис обертання кубітів.

- `1.01` основні поняття квантової фізики  
  *knowledge of the basic concepts of quantum physics*
- `1.02` динаміка кубітів  
  *knowledge of qubit dynamics*

**Оцінить важливість наступних УМІНЬ для формування компетентності з фізичних основ квантових технологій:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `1.03` визначати, чи знаходяться кубіти у пов’язаних (заплутаних) станах  
  *ability to determine whether qubits are in linked (entangled) states*
- `1.04` математично описувати стани та базиси Белла  
  *ability to describe Bell states and Bell bases mathematically*
- `1.05` математично описувати надщільне кодування  
  *ability to describe superdense coding mathematically*
- `1.06` математично описувати квантову телепортацію  
  *ability to describe quantum teleportation mathematically*
- `1.07` подавати кубіт на сфері Блоха  
  *ability to represent a qubit on the Bloch sphere*
- `1.08` застосовувати засоби перетворення квантових алгоритмів на керуючі імпульси для квантових комп’ютерів  
  *ability to apply tools that convert quantum algorithms into control pulses for quantum computers*

**Open question:** Які додаткові компетентності з фізичних основ квантових технологій, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 2: Математичні основи квантової інформатики (Mathematical foundations)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з математичних основ квантової інформатики:**  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain.

- основи теорії комплексних чисел: поняття комплексного числа, форми запису комплексних чисел, подання/відображення комплексного числа у комплексній площині;
- основи лінійної алгебри: задання векторів на площині та у просторі, операції над векторами; матриці, квадратні матриці, операції над матрицями, унітарні матриці;
- математика основ квантової фізики: бра-кет нотація, хвильова функція, когерентні стани, стани одиночних фотонів;
- статистична природа квантових вимірювань.

- `2.01` основи теорії комплексних чисел  
  *knowledge of the basics of complex-number theory*
- `2.02` основи лінійної алгебри  
  *knowledge of the basics of linear algebra*
- `2.03` математика основ квантової фізики  
  *knowledge of the mathematical foundations of quantum physics*
- `2.04` статистична природа квантових вимірювань  
  *knowledge of the statistical nature of quantum measurements*

**Оцінить важливість наступних УМІНЬ для формування компетентності з математичних основ квантової інформатики:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `2.05` пояснювати поняття уявної одиниці та комплексного числа, зображати комплексні числа у комплексній площині, здійснювати перехід від алгебраїчної форми подання до тригонометричної  
  *ability to explain the concepts of the imaginary unit and a complex number, to plot complex numbers in the complex plane, and to convert from algebraic to trigonometric form*
- `2.06` подавати вектори (матриці-стовпці, матриці-рядки) у бра-кет нотації  
  *ability to represent vectors (column matrices, row matrices) in bra-ket notation*
- `2.07` оперувати із стандартними базисами  
  *ability to work with standard bases*
- `2.08` подавати вектор у обраному базисі  
  *ability to represent a vector in a chosen basis*
- `2.09` перетворювати базис подавати вектор у обраному базисі векторного простору  
  *ability to transform a basis and represent a vector in a chosen basis of a vector space*
- `2.10` наводити приклади унітарних матриць та виконувати дії з ними  
  *ability to give examples of unitary matrices and to perform operations with them*

**Open question:** Які додаткові компетентності з математичних основ квантової інформатики, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 3: Забезпечувальні технології (Enabling technologies)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності із забезпечувальних технологій ***  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain (required).

- оптичні технології: класична оптика, лазери, оптоелектронні та оптомеханічні системи, джерела одиночних фотонів, джерела заплутаних фотонів, детектори на одиночних фотонах;
- лабораторні технології: аналіз шуму, технології чистих приміщень;
- експериментальне управління: програмне забезпечення, апаратне забезпечення, квантові алгоритми керування.

- `3.01` оптичні технології  
  *knowledge of optical technologies*
- `3.02` лабораторні технології  
  *knowledge of laboratory technologies*
- `3.03` експериментальне управління  
  *knowledge of experimental control*

**Оцінить важливість наступних УМІНЬ для формування компетентності із забезпечувальних технологій:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `3.04` розрізняти джерела фотонів  
  *ability to distinguish photon sources*
- `3.05` описувати типову структуру джерел одиночних та заплутаних фотонів  
  *ability to describe the typical structure of single-photon and entangled-photon sources*

**Open question:** Які додаткові компетентності із забезпечувальних технологій, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 4: Апаратне забезпечення квантових комп’ютерів та датчиків (Computer and sensor hardware)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з апаратного забезпечення квантових комп’ютерів та датчиків:**  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain.

- `4.01` пристрої на основі спіна: напівпровідникові квантові точки  
  *knowledge of the structure of spin-based devices (in particular, semiconductor quantum dots)*
- `4.02` нейтральні атоми та іони: іонні пастки  
  *knowledge of neutral atoms and ion traps*
- `4.03` нові види кубітів: молекулярно-спінові кубіти  
  *knowledge of new types of qubits (in particular, molecular spin qubits)*
- `4.04` обладнання для ініціалізації, маніпуляції та зчитування кубітів: мікрохвилі, лазери, резонатори (наприклад, зчитування та затвори надпровідних кубітів), вимикачі, фазоперемикачі, затримувачі  
  *knowledge of equipment for qubit initialisation, manipulation and readout (microwaves, lasers, resonators, switches, phase shifters, delay elements)*
- `4.05` використання апаратних платформ для квантових обчислень: порівняльний аналіз, інтеграція з класичним обладнанням  
  *knowledge of hardware platforms for quantum computing and of ways to integrate them with classical hardware*

**Оцінить важливість наступних УМІНЬ для формування компетентності з апаратного забезпечення квантових комп’ютерів та датчиків:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `4.06` описувати типові структури квантових комп’ютерів, пояснювати загальні принципи їх роботи  
  *ability to describe typical structures of quantum computers and to explain the general principles of their operation*
- `4.07` виконувати налаштування віддаленого доступу до квантових комп’ютерів  
  *ability to set up remote access to quantum computers*
- `4.08` виконувати квантові програми на квантових комп’ютерах  
  *ability to run quantum programs on quantum computers*

**Open question:** Які додаткові компетентності із апаратного забезпечення квантових комп’ютерів та датчиків, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 5: Квантові обчислення та моделювання (Computing and simulation)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з квантових обчислень та моделювання:**  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain.

- `5.01` квантові вентилі: однокубітні вентилі, двокубітні та багатокубітні вентилі  
  *knowledge of quantum gates (single-, two- and multi-qubit)*
- `5.02` квантові мови, засоби та платформи програмування: графічні платформи, середовище розробки програмного забезпечення, мови квантового програмування  
  *knowledge of quantum programming languages, quantum software development tools and platforms (including graphical ones)*
- `5.03` базові квантові алгоритми: алгоритм Шора, алгоритм Гровера, алгоритми квантової оптимізації, оцінка квантової фази, алгоритми квантової лінійної алгебри, квантові блукання, інші алгоритми  
  *knowledge of basic quantum algorithms (Shor's, Grover's, quantum optimisation, quantum phase estimation, quantum linear algebra, quantum walks and others)*
- `5.04` квантова корекція помилок: фізичні механізми декогерентності, код виправлення квантових похибок  
  *knowledge of quantum error correction (physical mechanisms of decoherence, correction of quantum errors)*
- `5.05` елементи квантового моделювання: цифрові квантові симулятори  
  *knowledge of elements of quantum simulation (in particular, digital quantum simulators)*

**Оцінить важливість наступних УМІНЬ для формування компетентності з квантових обчислень та моделювання:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `5.06` записувати квантові вентилі за допомогою унітарних матриць  
  *ability to write quantum gates as unitary matrices*
- `5.07` розрізняти та застосовувати однокубітні вентилі (перетворення Паулі, вентиль Адамара, фазові зсуви)  
  *ability to distinguish and apply single-qubit gates (Pauli transformations, Hadamard gate, phase shifts)*
- `5.08` виконувати операції за допомогою багатокубітних вентилів (CNOT, вентилі Тоффолі та Фредкіна)  
  *ability to perform operations with multi-qubit gates (CNOT, Toffoli and Fredkin gates)*
- `5.09` застосовувати квантові вентилі для запису квантових алгоритмів  
  *ability to apply quantum gates to write quantum algorithms*
- `5.10` послуговуватись мовами та засобами квантового програмування  
  *capacity to use quantum programming languages and tools*
- `5.11` реалізовувати квантові алгоритми (Шора, Гровера та ін.)  
  *ability to implement quantum algorithms (Shor's, Grover's, etc.)*
- `5.12` використовувати бібліотеки квантових алгоритмів оптимізації, машинного навчання, квантового блукання, квантового перетворення Фур’є та ін.  
  *ability to use libraries of quantum algorithms for optimisation, machine learning, quantum walks, the quantum Fourier transform, etc.*
- `5.13` застосовувати засоби квантової корекції помилок  
  *ability to apply quantum error-correction tools*
- `5.14` працювати із квантовими симуляторами  
  *ability to work with quantum simulators*

**Open question:** Які додаткові компетентності із квантових обчислень та моделювання, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 6: Квантові датчики та метрологія (Sensing and metrology)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з квантових датчиків та метрології ***  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain (required).

- атомні годинники;
- галузі застосування квантових датчиків: метрологія на одноквантовому рівні; медицина та молекулярна біологія; природні ресурси, цивільне будівництво та моніторинг Землі; транспорт і навігація; управління промисловими процесами.

- `6.01` атомні годинники  
  *knowledge of the structure of atomic clocks*
- `6.02` галузі застосування квантових датчиків  
  *knowledge of the fields of application of quantum sensors*

**Оцінить важливість наступних УМІНЬ для формування компетентності з квантових датчиків та метрології:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `6.03` описувати переваги та обмеження використання квантових датчиків (сенсорів) порівняно з іншими типами датчиків  
  *ability to describe the advantages and limitations of quantum sensors compared with other types of sensors*
- `6.04` пояснювати особливості будови атомних годинників  
  *ability to explain the structural features of atomic clocks*
- `6.05` наводити приклади застосування квантових датчиків у різних галузях  
  *ability to give examples of the application of quantum sensors in various fields*

**Open question:** Які додаткові компетентності із квантових датчиків та метрології, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 7: Квантова комунікація (Quantum communication)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з квантової комунікації:**  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain.

- `7.01` квантова криптографія: квантовий розподіл ключа, безпечна автентифікація, цифрові підписи, безпечне сховище; галузі застосування  
  *knowledge of quantum cryptography (quantum key distribution, secure authentication, digital signatures, fields of application)*
- `7.02` квантові мережі: квантовий Інтернет, сенсорні та годинникові мережі  
  *knowledge of quantum networks (quantum Internet, sensor and clock networks)*
- `7.03` інфраструктура та обладнання квантового зв’язку: волоконно-оптичні системи, бездротовий зв’язок, супутникові системи; квантові генератори випадкових чисел; квантова пам’ять, інтерфейси, комутатори; повторювачі, кінцеві вузли  
  *knowledge of quantum communication infrastructure and equipment (fibre-optic systems, wireless communication, satellite systems; quantum random number generators; quantum memory, interfaces, switches; repeaters, end nodes)*

**Оцінить важливість наступних УМІНЬ для формування компетентності з квантової комунікації:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `7.04` демонструвати роботу протоколів BB84, E91  
  *ability to demonstrate the operation of the BB84 and E91 protocols*
- `7.05` описувати корекцію помилок із квантовим кульбітом  
  *ability to describe error correction involving qubits*
- `7.06` послугуватись квантовими генераторами випадкових чисел  
  *ability to use quantum random number generators*
- `7.07` описувати принципи роботи та будову обладнання квантових мереж  
  *ability to describe the operating principles and structure of quantum network equipment*
- `7.08` наводити приклади застосування квантової криптографії у різних галузях  
  *ability to give examples of the application of quantum cryptography in various fields*

**Open question:** Які додаткові компетентності із квантової комунікації, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain 8: Практичні навички та загальні компетенції (Practical and general competencies)

**Оцінить важливість наступних ЗНАНЬ для формування компетентності з практичних навичок та загальних компетенцій:**  
*English:* Rate the importance of the following KNOWLEDGE for developing competence in this domain.

- `8.01` основи класичного (неквантового) програмування: мови програмування, алгоритми, класи складності, криптографія  
  *knowledge of the basics of classical (non-quantum) programming: programming languages, algorithms, complexity classes, cryptography*
- `8.02` застосування квантових технологій  
  *knowledge of the fields of application of quantum technologies*
- `8.03` загальні навички/компетенції: навички управління та лідерства (огляд, потенціал та обмеження, економічний вплив квантових технологій, підприємництво, розробка та реалізація проєкту); комунікація з експертами в галузі; дослідницька етика та відповідальність, інноваційність; знання про інтелектуальну власність, стандартизацію, сертифікацію  
  *knowledge of general skills/competences: management and leadership skills (overview, potential and limitations, economic impact of quantum technologies, entrepreneurship, project development and implementation); communication with experts in the field; research ethics and responsibility, innovativeness; knowledge of intellectual property, standardisation, certification*

**Оцінить важливість наступних УМІНЬ для формування компетентності з практичних навичків та загальних компетенцій:**  
*English:* Rate the importance of the following SKILLS for developing competence in this domain.

- `8.04` реалізовувати базові класичні алгоритми (зокрема криптографічні) мовами програмування  
  *ability to implement basic classical algorithms (in particular, cryptographic ones) in programming languages*
- `8.05` наводити приклади використання квантових алгоритмів для досягнення квантової переваги  
  *ability to give examples of the use of quantum algorithms to achieve quantum advantage*
- `8.06` демонструвати навички управління та лідерства, мережевої взаємодії та спілкування з експертами  
  *ability to demonstrate management and leadership skills, networking and communication with experts*

**Open question:** Які додаткові практичні навички та загальні компетенції, на Вашу думку, мають бути сформовані в шкільному курсі основ квантової інформатики?  
*English:* In your opinion, what additional competences in this domain should be developed in a school course on the fundamentals of quantum informatics? *Free-text answers are not released.*

## Domain importance (8 ratings, scale 0-5)

**Оцініть за шкалою від 0 до 5 важливість навчання у ліцеї:**  
*English:* Rate on a scale from 0 to 5 the importance of teaching the following at lyceum. Released as `domain_1` ... `domain_8`.

- `domain_1` фізичних основ квантових технологій (Physical foundations)
- `domain_2` математичних основ квантової інформатики (Mathematical foundations)
- `domain_3` забезпечувальних технологій (Enabling technologies)
- `domain_4` апаратного забезпечення квантових комп’ютерів та датчиків (Computer and sensor hardware)
- `domain_5` квантових обчислень та моделювання (Computing and simulation)
- `domain_6` квантових датчиків та метрології (Sensing and metrology)
- `domain_7` квантової комунікації (Quantum communication)
- `domain_8` практичних навичок та загальних компетенцій (Practical and general competencies)

## Respondent information

| Question (verbatim) | English | Options | Released |
|---|---|---|---|
| Оцініть свій рівень компетентності у квантовій інформатиці * | Rate your level of competence in quantum informatics (required) | маю початкові уявлення (I have initial ideas) = weight 1; обізнаний з окремими складовими (familiar with some components) = 2; глибоко обізнаний з окремими складовими (deeply familiar with some components) = 3; експерт (expert) = 4, chosen by nobody | Yes: `self_rated_competence`, `expertise_weight` |
| Ваша посада | Your position | студент (student), учитель (school teacher), науковий співробітник (researcher), викладач (university lecturer), інше (other; multiple choice) | No (quasi-identifier) |
| Стаж Вашої роботи * | Length of service (required) | до 5 років (up to 5 years), 5-10, 11-20, 21-30, 31-40, 41-50, понад 50 років (over 50) | No (quasi-identifier) |
| Ваша контактна адреса електронної пошти, побажання та зауваження. Вкажіть Ваш email, якщо Ви бажаєте отримати результати опитування | Your contact e-mail address, wishes and comments; give your e-mail if you wish to receive the survey results (optional) | free text | No (identifying) |

The export also records a submission timestamp. The timestamp, the eight open questions, position, length of service and the e-mail/comments field (12 columns in all) were removed by `revision/tools/deidentify_curriculum_responses.py` before release; see `README.md` in this folder.
