SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `knowledgetree`;
CREATE SCHEMA IF NOT EXISTS `knowledgetree` DEFAULT CHARACTER SET utf8 ;
USE `knowledgetree`;

-- -----------------------------------------------------
-- Table `knowledgetree`.`country`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`country` (
  `id` CHAR(10) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `country` */

insert  into `country`(`id`,`Name`) values ('Afghan','Afghanistan'),('Alb','Albania'),('Argent','Argentina'),('Armen','Armenia'),('Azer','Azerbaijan'),('BD','Bangladesh'),('Bolivia','Bolivia'),('Botswana','Botswana'),('Braz','Brazil'),('Chile','Chile'),('China','China'),('Croatia','Croatia'),('Czech','Czech Republic'),('Eritrea','Eritrea'),('Ethio','Ethiopia'),('Gambia','Gambia'),('Georgia','Georgia'),('Haiti','Haiti'),('Hungary','Hungary'),('ind','India'),('Indonesia','Indonesia'),('Iran','Iran'),('Iraq','Iraq'),('Israel','Israel'),('Japan','Japan'),('Kamp','Kampuchea'),('Kazakhstan','Kazakhstan'),('Kenya','Kenya'),('Kurd','Kurdistan'),('Kuwait','Kuwait'),('Lao','Lao'),('Lat','Latvia'),('Lith','Lithuania'),('Malay','Malaysia'),('Mali','Mali'),('Myanmar','Myanmar'),('Namibia','Namibia'),('NKorea','North Korea'),('Oman','Oman'),('Pakistan','Pakistan'),('Peru','Peru'),('Phil','Phillipines'),('Poland','Poland'),('Rumania','Rumania'),('Russia','Russia'),('SAfrica','South Africa'),('Saud','Saudi Arabia'),('Senegal','Senegal'),('Serbia','Serbia'),('Sing','Singapore'),('SKorea','South Korea'),('SL','Srilanka'),('Somalia','Somalia'),('Tadji','Tadjikistan'),('Tanz','Tanzania'),('Thai','Thailand'),('Turkey','Turkey'),('Turkmen','Turkmenistan'),('UAE','Emirates'),('Uganda','Uganda'),('Ukraine','Ukraine'),('Uzbek','Uzbekistan'),('Viet','Vietnam'),('Zimb','Zimbabwe');


-- -----------------------------------------------------
-- Table `knowledgetree`.`state`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`state` (
  `id` CHAR(10) NOT NULL ,
  `Country_id` CHAR(10) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`, `Country_id`) ,
  INDEX `fk_State_Country` (`Country_id` ASC) ,
  CONSTRAINT `fk_State_Country`
    FOREIGN KEY (`Country_id` )
    REFERENCES `knowledgetree`.`country` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `state` */

insert  into `state`(`id`,`Country_id`,`Name`) values ('AP','ind','Andhra pradesh'),('aru','ind','aruNAchal pradEsh'),('asm','ind','aSSAm'),('ben','ind','paschim bangAl'),('bih','ind','bihAr'),('Col','SL','Colombo'),('guj','ind','gujarAth'),('HP','ind','himAchal pradEsh'),('JK','ind','jammu & kAshmIr'),('kar','ind','karnAtaka'),('ker','ind','kEraLa'),('mani','ind','maNipUr'),('megh','ind','mEghAlay'),('MH','ind','mahA rAshTRa'),('miz','ind','mizOram'),('MP','ind','madhya pradEsh'),('naga','ind','nAgAland'),('ND','ind','New Delhi'),('odi','ind','odiSSa'),('punj','ind','punJab'),('raj','ind','rAjAsTHAn'),('sik','ind','sikkim'),('TN','ind','tamiL NADu'),('tri','ind','tripura'),('UP','ind','utthara pradEsh');

-- -----------------------------------------------------
-- Table `knowledgetree`.`city`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`city` (
  `id` CHAR(10) NOT NULL ,
  `State_id` CHAR(10) NOT NULL ,
  `Country_id` CHAR(10) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`, `State_id`, `Country_id`) ,
  INDEX `fk_City_State` (`State_id` ASC, `Country_id` ASC) ,
  CONSTRAINT `fk_City_State`
    FOREIGN KEY (`State_id` , `Country_id` )
    REFERENCES `knowledgetree`.`state` (`id` , `Country_id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `city` */

insert  into `city`(`id`,`State_id`,`Country_id`,`Name`) values ('ahmed','guj','ind','Ahmedabad'),('allah','UP','ind','Allahabad'),('bho','MP','ind','Bhopal'),('bhuv','odi','ind','Bhuvaneshwar'),('bidar','kar','ind','Bidar'),('blr','kar','ind','Bangalore'),('che','TN','ind','Chennai'),('hyd','AP','ind','Hyderabad'),('jai','raj','ind','Jaipur'),('kol','ben','ind','Kolkata'),('luck','UP','ind','Lucknow'),('mumb','MH','ind','Mumbai'),('mys','kar','ind','Mysore'),('nd','ND','ind','New Delhi'),('pat','bih','ind','Patna'),('pune','MH','ind','Pune'),('puri','odi','ind','Puri'),('sim','HP','ind','Simla'),('Tanj','TN','ind','thanjAvUr'),('uday','raj','ind','Udaipur'),('vizag','AP','ind','Vishakapatnam');

-- -----------------------------------------------------
-- Table `knowledgetree`.`district`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`district` (
  `id` CHAR(10) NOT NULL ,
  `State_id` CHAR(10) NOT NULL ,
  `Country_id` CHAR(10) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`, `State_id`, `Country_id`) ,
  INDEX `fk_District_State` (`State_id` ASC, `Country_id` ASC) ,
  CONSTRAINT `fk_District_State`
    FOREIGN KEY (`State_id` , `Country_id` )
    REFERENCES `knowledgetree`.`state` (`id` , `Country_id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `district` */

insert  into `district`(`id`,`State_id`,`Country_id`,`Name`) values ('Gul','kar','ind','Gulbarga'),('mandya','kar','ind','Mandya'),('tumkur','kar','ind','Tumkur');


-- -----------------------------------------------------
-- Table `knowledgetree`.`person`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person` (
  `id` CHAR(20) NOT NULL ,
  `First` CHAR(30) NOT NULL ,
  `Middle` CHAR(30) NULL DEFAULT NULL ,
  `Last` CHAR(30) NULL DEFAULT NULL ,
  `Initials` CHAR(10) NULL DEFAULT NULL ,
  `Nick` CHAR(20) NULL DEFAULT NULL ,
  `Other` CHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Persons';

/*Data for the table `person` */

insert  into `person`(`id`,`First`,`Middle`,`Last`,`Initials`,`Nick`,`Other`) values ('ama','Ananth',NULL,'M.A.','AMA',NULL,NULL),('hem','Hemanth',NULL,NULL,'H',NULL,NULL),('maa','Alwar',NULL,'M.A.','MAA',NULL,NULL),('mal','Lakshmitathachar',NULL,'M.A.','MAL',NULL,NULL),('ND','Nikhil','','Desale','ND','',''),('nmg','Narasimhan',NULL,'M.G.','NMG','Naras',NULL),('pa','Pavitha',NULL,'A.','PA',NULL,NULL),('sd','Sindhu',NULL,'D.','SD',NULL,NULL),('skv','Surekha',NULL,'K.V.','SKV',NULL,NULL),('vr','Vinay',NULL,'R.','VR',NULL,NULL),('vs','Vijay',NULL,'Srinivas','VS',NULL,NULL);


-- -----------------------------------------------------
-- Table `knowledgetree`.`address`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`address` (
  `id` CHAR(20) NOT NULL ,
  `Value` VARCHAR(500) NULL DEFAULT NULL ,
  `HouseNumber` CHAR(30) NULL DEFAULT NULL ,
  `Street` CHAR(30) NULL DEFAULT NULL ,
  `Area` CHAR(30) NULL DEFAULT NULL ,
  `City_id` CHAR(10) NULL DEFAULT NULL ,
  `City_State_id` CHAR(10) NULL DEFAULT NULL ,
  `City_Country_id` CHAR(10) NULL DEFAULT NULL ,
  `District_id` CHAR(10) NULL DEFAULT NULL ,
  `District_State_id` CHAR(10) NULL DEFAULT NULL ,
  `District_Country_id` CHAR(10) NULL DEFAULT NULL ,
  `Person` CHAR(20) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Address_City` (`City_id` ASC, `City_State_id` ASC, `City_Country_id` ASC) ,
  INDEX `fk_Address_District` (`District_id` ASC, `District_State_id` ASC, `District_Country_id` ASC) ,
  INDEX `fk_Address_Person` (`Person` ASC) ,
  CONSTRAINT `fk_Address_City`
    FOREIGN KEY (`City_id` , `City_State_id` , `City_Country_id` )
    REFERENCES `knowledgetree`.`city` (`id` , `State_id` , `Country_id` )
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Address_District`
    FOREIGN KEY (`District_id` , `District_State_id` , `District_Country_id` )
    REFERENCES `knowledgetree`.`district` (`id` , `State_id` , `Country_id` )
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Address_Person`
    FOREIGN KEY (`Person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`language`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`language` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `UnicodeBlock` MEDIUMINT(9) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Langauges for the works, commentaries etc';

/*Data for the table `language` */

insert  into `language`(`id`,`Name`,`UnicodeBlock`) values ('aSSAmi','aSSAmi',21),('bengAli','bengAli',21),('English','English',2),('gujarAthi','gujarAthi',23),('hindi','hindi',20),('kannaDa','KannaDa',27),('kashmIri','kashmIri',185),('malayALam','malayALam',28),('mANipuri','mANipuri',136),('marATHi','marATHi',20),('oDiyA','oDiyA',24),('punjAbi','punJabi',22),('Samskrth','Samskrth',20),('tamiL','tamiL',25),('telugu','telugu',26),('urdu','urdu',19);

-- -----------------------------------------------------
-- Table `knowledgetree`.`affiliation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`affiliation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'An institution that a person is affiliated with';

/*Data for the table `affiliation` */

insert  into `affiliation`(`id`,`Name`) values ('SRVVP','Sri Ramanuja Vishwa Vidya Pratishtana');

-- -----------------------------------------------------
-- Table `knowledgetree`.`personlife`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`personlife` (
  `id` CHAR(10) NOT NULL ,
  `Living` TINYINT(1) NULL DEFAULT '1' ,
  `Birth` DATE NULL DEFAULT NULL ,
  `Death` DATE NULL DEFAULT NULL ,
  `Period` CHAR(25) NULL DEFAULT NULL ,
  `History` VARCHAR(255) NULL DEFAULT NULL ,
  `Life` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_PersonLife_Person` (`id` ASC) ,
  CONSTRAINT `fk_PersonLife_Person`
    FOREIGN KEY (`id` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'The life of a person. May be a historical, fictional or even a mytholgical person';


-- -----------------------------------------------------
-- Table `knowledgetree`.`role`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`role` (
  `id` CHAR(20) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'A person can be an Author, Scholar, Reviewer etc';

/*Data for the table `role` */

insert  into `role`(`id`,`Name`) values ('Auth','Author'),('Edt','Editor'),('Mgr','Manager'),('Mtd','Metadata Manager'),('pub','Publisher'),('Rev','Reviewer'),('Sch','Scholar'),('Scr','Scribe');

-- -----------------------------------------------------
-- Table `knowledgetree`.`script`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`script` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `UnicodeBlock` MEDIUMINT(9) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Scripts for the works, commentaries etc';

/*Data for the table `script` */

insert  into `script`(`id`,`Name`,`UnicodeBlock`) values ('bengAli','bengAli',21),('brAhmi','brAhmi',181),('devanAgari','devanAgari',20),('granTHa','granTHa',NULL),('gujarAthi','gujarAthi',23),('gurmukhi','gurmukhi',22),('kannaDa','kannADa',27),('malayALam','malayALam',28),('oDiyA','oDiyA',24),('shArada','shArada',185),('tamiL','tamiL',25),('telugu','telugu',26);


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject` (
  `id` CHAR(20) NOT NULL ,
  `Name` CHAR(30) NOT NULL ,
  `Description` VARCHAR(5000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `subject` */

insert  into `subject`(`id`,`Name`,`Description`) values ('agama','agama','agamas are procedures for wrship, rites/rituals and yajnas'),('Aitreya','Aitreya','Aitreyopanishad  \"The Microcosm of Man\"'),('AraNyaka','AraNyaka',' \"wilderness texts\" or \"forest treaties\"'),('aTHarvaNa','AtharvaNa Veda','The Atharvaveda (Sanskrit: अथर्ववेद, Atharvaveda from atharv??as and veda meaning \'knowledge\') is the \'knowledge storehouse of atharv??as, the procedures for everyday life\'. The text is the fourth Veda, but has been a late addition to the Vedic scriptures of Hinduism.\nThe Atharvaveda is composed in Vedic Sanskrit, and it is a collection of 730 hymns with about 6,000 mantras, divided into 20 books. About a sixth of the Atharvaveda text adapts verses from the Rigveda, and except for Books 15 and 16, the text is in poem form deploying a diversity of Vedic meters. Two different recensions of the text - the Paippal?da and the ?aunak?ya - have survived into modern times. Reliable manuscripts of the Paippalada edition were believed to have been lost, but a well preserved version was discovered among a collection of palm leaf manuscripts in Odisha in 1957.\nThe Atharvaveda is sometimes called the \'Veda of magical formulas\', an epithet declared to be incorrect by other scholars. The Samhita layer of the text likely represents a developing 2nd millennium BCE tradition of magico-religious rites to address superstitious anxiety, spells to remove maladies believed to be caused by demons, and herbs- and nature-derived potions as medicine. Many books of the Atharvaveda Samhita are dedicated to rituals without magic and to theosophy. The text, states Kenneth Zysk, is one of oldest surviving record of the evolutionary practices in religious medicine and reveals the \'earliest forms of folk healing of Indo-European antiquity\'.\nIt was likely compiled as a Veda contemporaneously with Samaveda and Yajurveda, or about 1200 BC - 1000 BC. Along with the Samhita layer of text, the Atharvaveda includes a Brahmana text, and a final layer of the text that covers philosophical speculations. The latter layer of Atharvaveda text includes three primary Upanishads, influential to various schools of Hindu philosophy. These include the Mundaka Upanishad, the Mandukya Upanishad and the Prashna Upanishad.\n'),('aum','औं','औं - The Primary Sound'),('Ayurveda','Ayurveda','Indian Medical Systems'),('bhel','bhel samhita',''),('BrahadAraN','BrahadAraNyaka','the big forest treatise'),('BrahmaNa','BrahmaNa','Prose commentaries on Samhitas'),('Chandas','Chandas','Metre'),('Chandogya','Chandogya','Chandogyopanishad \"Song and Sacrifice\"'),('Darshanas','Darshanas','There are six Darshanas - Total glimpse of the Vedas'),('dhanur','dhanur veda','An upaveda of Rk Veda'),('Dhanurveda','Dhanurveda','Archery'),('dravida','dravida vedas','Dravida Vedas are subjects in tamizh (maNipravalam) which parallel the Vedas'),('gandharva','gandahrva veda','An upaveda of sama veda'),('Gandharvav','Gandharva veda','Sacred Music and Dance'),('harita','harita samhita',''),('Isa','Isa','Isopanishad \"The Inner Ruler\"'),('Jyotisha','Jyotisha','Astronomy/Astrology/Cosmology'),('Kalpa','Kalpa','Ritual'),('kashyapa','kashyapa samhita',''),('Katha','Katha','Kathopanishad \"Death as Teacher\"'),('Kena','Kena','Kenopanishad \"Who moves the world?\"'),('KrishnaYajur','Krishna Yajurveda','There are four surviving recensions of the Krishna Yajurveda - Taittir?ya sa?hit?, Maitrayani sa?hit?, Ka?ha sa?hit? and Kapi??hala sa?hit? . A total of eighty six recensions are mentioned to exist in Vayu Purana, however vast majority of them are believed to be lost.  The Katha school is referred to as a sub-school ofCarakas (wanderers) in some ancient texts of India, because they did their scholarship as they wandered from place to place.'),('mAndukya','mAndukya','mAndukyopanishad \"Consciousness and its phases\"'),('Mundaka','Mundaka','Mundakopanoishad  \"Two modes of Knowing\"'),('Nirukta','Nirukta','Etymology'),('Periyatiruvandathi','Periya tiruvandathi',''),('Poorva','Poorva Mimamsa','Darshana -  Glimpse of Divinity'),('Prasna','Prasna','Prasnopanishad  \"The Breath of Life\"'),('RkVeda','Rk Veda','The Rigveda (Sanskrit: ऋग्वेद ṛgveda, from  \'praise, shine\' and veda \'knowledge\') is an ancient Indian collection of Vedic Sanskrit hymns. It is one of the four canonical sacred texts (?ruti) of Hinduism known as the Vedas. The text is a collection of 1,028 hymns and 10,600 verses, organized into ten books (Mandalas). The hymns are dedicated to Rigvedic deities.\nThe Rigveda begins with a small book addressed to deity Agni, Indra and other gods, all arranged according to decreasing total number of hymns in each deity collection; for each deity series the hymns progress from longer to shorter ones; yet, the number of hymns per book increases; finally, the meter is systematically arranged from jagati and tristubh to anustubh and gayatri as the text progresses. In terms of substance, the hymns predominantly discuss cosmology and praise deities in the earliest composed eight books, shifting in books 1 and 10, that were added last, to philosophical or speculative questions about the origin of the universe and the nature of god, the virtue of D?na (charity) in society, and other metaphysical issues in its hymns.\nRigveda is one of the oldest extant texts in any Indo-European language. Philological and linguistic evidence indicate that the Rigveda was composed in the north-western region of the Indian subcontinent, most likely between c. 1500-1200 BC, though a wider approximation of c. 1700-1100 BC has also been given.\nSome of its verses continue to be recited during Hindu rites of passage celebrations such as weddings and religious prayers, making it probably the world\'s oldest religious text in continued use.'),('sAmaVeda','sAma Veda','The Samaveda (Sanskrit: ??????, s?maveda, from s?man \'song\' and veda \'knowledge\'), is the Veda of melodies and chants. It is an ancient Vedic Sanskrit text, and part of the scriptures of Hinduism. One of the four Vedas, it is a liturgical text whose 1,875 verses are primary derived from the Rigveda. Three recensions of the Samaveda have survived, and variant manuscripts of the Veda have been found in various parts of India.\nWhile its earliest parts are believed to date from as early as 1700 BCE (the Rigvedic period), the existing compilation dates from the post-Rigvedic Mantra period of Vedic Sanskrit, c. 1200 or 1000 BCE, but roughly contemporary with the Atharvaveda and the Yajurveda.\nEmbedded inside the Samaveda is the widely studied Chandogya Upanishad and Kena Upanishad, considered as primary Upanishads and as influential on the six schools of Hindu philosophy, particularly the Vedanta school. The classical Indian music and dance tradition considers the chants and melodies in Samaveda as one of its roots.\nIt is also referred to as Sama Veda or Samveda.'),('Samhita','Samhita','Collection of metric texts'),('Samkhya','Samkhya','Darshana -  Glimpse of Divinity'),('ShastrashA','ShastrashAstra','Military Knowledge'),('Shiksha','Shiksha','Phonetics'),('ShilpashAs','Shilpa shAstra',NULL),('ShuklaYajur','Shukla Yajurveda','The samhita in the Shukla Yajurveda is called the Vajasaneyi Samhita. The name Vajasaneyi is derived from Vajasaneya, patronymic of sage Yajnavalkya , and the founder of the Vajasaneyi branch. There are two (nearly identical) surviving recensions of the Vajasaneyi Samhita (VS): Vajasaneyi Madhyandina and Vajasaneyi Kanva. The lost recensions of White Yajurveda, mentioned in other texts of ancient India, include Jabala, Baudhya, Sapeyi, Tapaniya, Kapola, Paundravatsa,Avati, Paramavatika, Parasara, Vaineya, Vaidheya, Katyayana and Vaijayavapa.[14] \r\n'),('sthapatya','sthapatya veda','An upaveda of Rk Veda'),('Sthapatyav','Sthapatyaveda','Architecture (temples)'),('TaittirIya','TaittirIya','Taittiriyopanishad  \"From Food to Joy\"'),('tiruvasiriyam','tiruvasiriyam',''),('tiruvirutham','tiruvirutham',''),('tiruvoimozhi','tiruvoimozhi',''),('Upanishad','Upanishad','Fundamental philosophy explains Vedas'),('Uttara','Uttara Mimamsa','Darshana -  Glimpse of Divinity'),('Vaishesh','Nyaya Vaisheshika','Darshana'),('Veda','Veda','Vedas (Sanskrit: वेद veda, \'knowledge\') are a large body of texts originating in ancient India. Composed in Vedic Sanskrit, the texts constitute the oldest layer of Sanskrit literature and the oldest scriptures of Hinduism. Hindus consider the Vedas to be apauru?eya, which means \'not of a man, superhuman and \'impersonal, authorless\'. '),('Vedanga','Vedanga','Veda Angas:\r\n	The Vedanga (ved??ga, \'limbs of the Veda\') are six auxiliary disciplines in Hinduism that are traditionally associated with the study and understanding of the Vedas (texts from the Vedic period). these are also do in swadhyay These are:\r\nShiksha (?ik??): phonetics, phonology and morphophonology (sandhi)\r\nKalpa (kalpa): ritual\r\nVyakarana (vy?kara?a): grammar\r\nNirukta (nirukta): etymology\r\nChandas (chandas): meter\r\nJyotisha (jyoti?a): Time measurement, forecasting movement of Sun, Moon and planetary movement, astronomy\r\n	The Vedangas are first mentioned in the Mundaka Upanishad (at 1.1.5) as subjects for students of the Vedas. Later, they developed into independent disciplines, each with its own corpus of Sutras. Traditionally, vyakarana and nirukta are common to all four vedas, while each veda has its own shiksha, chandas, kalpa and jyotisha texts.\r\n	Shiksha is the first discipline and scripture existing to teach morphophonology, phonetics, and phonology. Shiksha has 32 systems regarding these, each of which differently relate to the Vedas. It shows that a large amount of time during the Vedic period was devoted to respecting religious pronunciation and recitation. Kalpa is the second discipline and scripture existing to teach rituals and is considered aphoristic.Vyakarana is the third discipline and scripture devoted to grammar, and is considered to be a heavily important part of the Vedanga. Vyakarana is believed to be the \'mouth among the Vedang\'. Nirukta is the fourth discipline and scripture and is devoted to etymology, and is sometimes thought of as part of Vyakarana. Chandas is the fifth discipline and scripture and is devoted to Sanskrit prosody. Jyotisha is the final discipline and scripture and is devoted to the measurement of time, forecasting the movement of planets, the Sun and the Moon, and astronomy.'),('Vedantha','Vedantha','Darshana -  \"End of the vedas\" - sum of all knowledge'),('VyAkaraNa','VyAkaraNa','Grammar'),('YajurVeda','Yajur Veda','The Yajurveda (Sanskrit: ????????, yajurveda, from yajus meaning \'prose mantra\' and veda meaning \'knowledge\') is the Veda of prose mantras. An ancient Vedic Sanskrit text, it is a compilation of ritual offering formulas that were said by a priest while an individual performed ritual actions such as those before the yajna fire. Yajurveda is one of the four Vedas, and one of the scriptures of Hinduism. The exact century of Yajurveda\'s composition is unknown, and estimated by scholars to be around 1200 to 1000 BCE, contemporaneous with Samaveda and Atharvaveda.\nThe Yajurveda is broadly grouped into two - the \'black\' (Krishna) Yajurveda and the \'white\' (Shukla) Yajurveda. The term \'black\' implies \'the un-arranged, unclear, motley collection\' of verses in Yajurveda, in contrast to the \'white\' which implies the \'well arranged, clear\' Yajurveda. The black Yajurveda has survived in four recensions, while two recensions of white Yajurveda has survived into the modern times.\nThe earliest and most ancient layer of Yajurveda samhita includes about 1,875 verses, that are distinct yet borrow and build upon the foundation of verses in Rigveda. The middle layer includes the Satapatha Brahmana, one of the largest Brahmana texts in the Vedic collection. The youngest layer of Yajurveda text includes the largest collection of primary Upanishads, influential to various schools of Hindu philosophy. These include the Brihadaranyaka Upanishad, the Isha Upanishad, the Taittiriya Upanishad, the Katha Upanishad, the Shvetashvatara Upanishad and the Maitri Upanishad.\n'),('Yoga','Yoga','Darshana -  Glimpse of Divinity');


-- -----------------------------------------------------
-- Table `knowledgetree`.`work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work` (
  `id` CHAR(20) NOT NULL ,
  `Title` VARCHAR(45) NULL DEFAULT NULL ,
  `Description` VARCHAR(5000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `work` */

insert  into `work`(`id`,`Title`,`Description`) values ('BhagavadGeetha','Bhagavad Geetha','The Song Celestial by Lord KrishNa'),('ShreeBhashyam','Shree Bhashyam','Shree rAmAnuja\'s Comprehensive Treatise on Brahman'),('SiddhantaKaumudi','Siddhanta Kaumudi','A Kaumudi on Siddhantas :-)'),('VivekaChoodAmaNi','Viveka ChoodAmaNi','The Source of Spiritual Wisdom');

-- -----------------------------------------------------
-- Table `knowledgetree`.`work_subject_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_subject_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(45) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `work_subject_relation` */

insert  into `work_subject_relation`(`id`,`Name`,`Description`) values ('comcom','Commentary on Commentary','Secondary commentary'),('commentary','Commentary','Commentary on subject'),('compile','Compilation','Compilation of other works'),('original','Original Work','Original Work on subject'),('recitation','Recitation','Recitation (audio/video) of a work'),('subcomment','Sub-commentary','Sub-commentary on subject'),('translate','Translation','Translation of another work'),('treatise','Treatise','Treatise on subject'),('Upabrahmya','Upabrahmya - Upabrahmana','Upabrahmya - Upabrahmana Bhava (Explanation - Explained Object)'),('vritthi','Vritthi','??????');

-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_has_work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_has_work` (
  `Subject` CHAR(20) NOT NULL ,
  `Work` CHAR(20) NOT NULL ,
  `work_subject_relation` CHAR(20) NOT NULL ,
  PRIMARY KEY (`Subject`, `Work`, `work_subject_relation`) ,
  INDEX `fk_Subject_has_Work_Subject` (`Subject` ASC) ,
  INDEX `fk_Subject_has_Work_Work` (`Work` ASC) ,
  INDEX `fk_subject_has_work_work_subject_relation` (`work_subject_relation` ASC) ,
  CONSTRAINT `fk_Subject_has_Work_Subject`
    FOREIGN KEY (`Subject` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Subject_has_Work_Work`
    FOREIGN KEY (`Work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_has_work_work_subject_relation`
    FOREIGN KEY (`work_subject_relation` )
    REFERENCES `knowledgetree`.`work_subject_relation` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `subject_has_work` */

insert  into `subject_has_work`(`Subject`,`Work`,`work_subject_relation`) values ('Chandogya','BhagavadGeetha','commentary'),('RkVeda','BhagavadGeetha','treatise'),('Samkhya','BhagavadGeetha','treatise'),('Vaishesh','ShreeBhashyam','commentary'),('Veda','BhagavadGeetha','treatise'),('VyAkaraNa','ShreeBhashyam','commentary'),('Yoga','BhagavadGeetha','treatise'),('Yoga','ShreeBhashyam','commentary');


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_subject_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_subject_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


/*Data for the table `subject_subject_relation` */

insert  into `subject_subject_relation`(`id`,`Name`,`Description`) values ('Adhaara','Adhaara - Adhaari','Adhaara - Adhaari (support - supoorted)'),('Anga','Anga-Angi','Anga - Angi Bhava (Main-Subsidiary relation)'),('Anonya','Anonya Ashraya','Anonya - Ashraya Bhava (mutual dependence)'),('Ashraya','Ashraya - Ashreyi','Ashraya - Ashreyi Bhava (substrate - subtratum)'),('Avayavi','Avayavi','Avayava-Avayavi Bhava (Part/Whole Relation)'),('darshana','Darshana','Glimpse of Divinity'),('Dharma','Dharma - Dharmi','Dharma - Dharmi (Attribute - Substantive)'),('Janya','Janya-Janaka','Janya - Janaka Bhava (born of - given birth to)'),('Kaarya','Kaarya - Kaarana','Kaarya - Kaarana Bhava (cause - effect)'),('Nirupaka','Nirupya - Nirupaka','Nirupya - Nirupaka Bhava (characterized - character)'),('parentchil','Avayavi','Avayava-Avayavi Bhava (Parent/Child Relation)'),('part','Anga','Anga - Angi Bhava (Part-Whole relation)'),('Prakaara','Prakaara-Prakaari','Prakaara-Prakaari (Qualification - Quailificant)'),('sibling','Common Parent','The two subjects are related by a common parent subject'),('Uddheshya','Uddheshya - Vidheya','Uddheshya - Vidheya Bhava (predication - predicated)'),('upa','Upaveda','Subsidiary branches of Vedas'),('Upabrahmya','Upabrahmya - Upabrahmana','Upabrahmya - Upabrahmana (explanatory-explanation)'),('upani','Upanishad','Description of Vedas'),('Vishaya','Vishaya - Vishayi','Vishaya - Vishayi Bhava (Knowledge subject - Knowledge object)');


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_relatesto_subject`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_relatesto_subject` (
  `Subject1` CHAR(20) NOT NULL ,
  `Subject2` CHAR(20) NOT NULL ,
  `relation_id` CHAR(20) NULL DEFAULT NULL ,
  `sortorder` SMALLINT NULL COMMENT 'Each subject2 has a sequence in its relation to subject1 (1,2,3). Used for sorting the subtree.' ,
  PRIMARY KEY (`Subject1`, `Subject2`) ,
  INDEX `fk_subject_has_subject_subject` (`Subject1` ASC) ,
  INDEX `fk_subject_has_subject_subject1` (`Subject2` ASC) ,
  INDEX `fk_subject_relatesto_subject_subject_subject_relation` (`relation_id` ASC) ,
  CONSTRAINT `fk_subject_has_subject_subject`
    FOREIGN KEY (`Subject1` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_has_subject_subject1`
    FOREIGN KEY (`Subject2` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_relatesto_subject_subject_subject_relation`
    FOREIGN KEY (`relation_id` )
    REFERENCES `knowledgetree`.`subject_subject_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

/*Data for the table `subject_relatesto_subject` */

insert  into `subject_relatesto_subject`(`Subject1`,`Subject2`,`relation_id`,`sortorder`) values ('aTHarvaNa','Ayurveda','upa',1),('aTHarvaNa','Dhanurveda','upa',2),('aum','agama','Anga',2),('aum','dravida','Anga',3),('aum','Veda','Janya',1),('Darshanas','Poorva','darshana',6),('Darshanas','Samkhya','darshana',2),('Darshanas','Uttara','darshana',7),('Darshanas','Vaishesh','darshana',3),('Darshanas','Vedantha','darshana',8),('Darshanas','Yoga','darshana',4),('dravida','Periyatiruvandathi','Anga',NULL),('dravida','tiruvasiriyam','Anga',NULL),('dravida','tiruvirutham','Anga',NULL),('dravida','tiruvoimozhi','Anga',NULL),('sAmaVeda','Gandharvav','upa',NULL),('Samhita','bhel','Avayavi',NULL),('Samhita','harita','Avayavi',NULL),('Samhita','kashyapa','Avayavi',NULL),('ShuklaYajur','BrahmaNa','Janya',2),('ShuklaYajur','Samhita','Janya',1),('Upanishad','AraNyaka','Janya',NULL),('Upanishad','BrahadAraN','Janya',NULL),('Upanishad','Isa','Janya',NULL),('Upanishad','Katha','Janya',NULL),('Upanishad','Kena','Janya',NULL),('Upanishad','mAndukya','Janya',NULL),('Upanishad','Mundaka','Janya',NULL),('Upanishad','Prasna','Janya',NULL),('Veda','aTHarvaNa','Janya',4),('Veda','Darshanas','Vishaya',6),('Veda','RkVeda','Janya',1),('Veda','sAmaVeda','Janya',3),('Veda','Upanishad','upani',7),('Veda','Vedanga','Anga',5),('Veda','YajurVeda','Janya',2),('Vedanga','Chandas','Anga',6),('Vedanga','Jyotisha','Anga',5),('Vedanga','Kalpa','Anga',4),('Vedanga','Nirukta','Anga',3),('Vedanga','Shiksha','Anga',1),('YajurVeda','KrishnaYajur','Anga',2),('YajurVeda','ShuklaYajur','Anga',1);



-- -----------------------------------------------------
-- Table `knowledgetree`.`tag`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`tag` (
  `id` VARCHAR(255) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  `BelongsTo` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Tag_Tag` (`BelongsTo` ASC) ,
  CONSTRAINT `fk_Tag_Tag`
    FOREIGN KEY (`BelongsTo` )
    REFERENCES `knowledgetree`.`tag` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Tags are additional metadata. They can be used in search and filter for subjects, works and persons. They can be managed by a Metadata Manager';


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_has_affiliation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_has_affiliation` (
  `person` CHAR(20) NOT NULL ,
  `affiliation` CHAR(20) NOT NULL ,
  PRIMARY KEY (`person`, `affiliation`) ,
  INDEX `fk_person_has_Affiliation_person` (`person` ASC) ,
  INDEX `fk_person_has_Affiliation_Affiliation` (`affiliation` ASC) ,
  CONSTRAINT `fk_person_has_Affiliation_person`
    FOREIGN KEY (`person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_person_has_Affiliation_Affiliation`
    FOREIGN KEY (`affiliation` )
    REFERENCES `knowledgetree`.`affiliation` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

/*Data for the table `person_has_affiliation` */

insert  into `person_has_affiliation`(`person`,`affiliation`) values ('ama','SRVVP');

-- -----------------------------------------------------
-- Table `knowledgetree`.`work_in_language`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_in_language` (
  `work` CHAR(20) NOT NULL ,
  `language` CHAR(20) NOT NULL ,
  `location` VARCHAR(255) NULL COMMENT 'Physical location URL' ,
  PRIMARY KEY (`work`, `language`) ,
  INDEX `fk_work_has_language_work` (`work` ASC) ,
  INDEX `fk_work_has_language_language` (`language` ASC) ,
  CONSTRAINT `fk_work_has_language_work`
    FOREIGN KEY (`work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_work_has_language_language`
    FOREIGN KEY (`language` )
    REFERENCES `knowledgetree`.`language` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

/*Data for the table `work_in_language` */

insert  into `work_in_language`(`work`,`language`,`location`) values ('BhagavadGeetha','English',NULL),('BhagavadGeetha','kannaDa',NULL),('BhagavadGeetha','Samskrth',NULL),('ShreeBhashyam','Samskrth',NULL),('ShreeBhashyam','tamiL',NULL),('SiddhantaKaumudi','Samskrth',NULL),('VivekaChoodAmaNi','Samskrth',NULL);

-- -----------------------------------------------------
-- Table `knowledgetree`.`work_in_script`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_in_script` (
  `work` CHAR(20) NOT NULL ,
  `script` CHAR(20) NOT NULL ,
  `location` VARCHAR(255) NULL COMMENT 'Physical location URL' ,
  PRIMARY KEY (`work`, `script`) ,
  INDEX `fk_work_has_script_work` (`work` ASC) ,
  INDEX `fk_work_has_script_script` (`script` ASC) ,
  CONSTRAINT `fk_work_has_script_work`
    FOREIGN KEY (`work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_work_has_script_script`
    FOREIGN KEY (`script` )
    REFERENCES `knowledgetree`.`script` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

/*Data for the table `work_in_script` */

insert  into `work_in_script`(`work`,`script`,`location`) values ('BhagavadGeetha','devanAgari',NULL),('BhagavadGeetha','granTHa',NULL),('BhagavadGeetha','kannaDa',NULL),('ShreeBhashyam','devanAgari',NULL),('ShreeBhashyam','shArada',NULL),('SiddhantaKaumudi','devanAgari',NULL),('VivekaChoodAmaNi','devanAgari',NULL);


-- -----------------------------------------------------
-- Table `knowledgetree`.`tagSubject`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`tagSubject` (
  `id` VARCHAR(255) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  `BelongsTo` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_TagSubject_TagSubject` (`BelongsTo` ASC) ,
  CONSTRAINT `fk_TagSubject_TagSubject`
    FOREIGN KEY (`BelongsTo` )
    REFERENCES `knowledgetree`.`tagSubject` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Tags are additional metadata. They can be used in search and filter for subjects, works and persons. They can be managed by a Metadata Manager';


-- -----------------------------------------------------
-- Table `knowledgetree`.`tagWork`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`tagWork` (
  `id` VARCHAR(255) NOT NULL ,
  `Name` CHAR(30) NULL DEFAULT NULL ,
  `BelongsTo` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_TagWork_TagWork` (`BelongsTo` ASC) ,
  CONSTRAINT `fk_TagWork_TagWork`
    FOREIGN KEY (`BelongsTo` )
    REFERENCES `knowledgetree`.`tagWork` (`id` )
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Tags are additional metadata. They can be used in search and filter for subjects, works and persons. They can be managed by a Metadata Manager';


-- -----------------------------------------------------
-- Table `knowledgetree`.`subject_has_tag`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`subject_has_tag` (
  `subject` CHAR(20) NOT NULL ,
  `tag` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`subject`, `tag`) ,
  INDEX `fk_subject_has_tagSubject_subject` (`subject` ASC) ,
  INDEX `fk_subject_has_tagSubject_tagSubject` (`tag` ASC) ,
  CONSTRAINT `fk_subject_has_tagSubject_subject`
    FOREIGN KEY (`subject` )
    REFERENCES `knowledgetree`.`subject` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_subject_has_tagSubject_tagSubject`
    FOREIGN KEY (`tag` )
    REFERENCES `knowledgetree`.`tagSubject` (`id` )
    ON DELETE NO ACTION
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_has_tag`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_has_tag` (
  `work` CHAR(20) NOT NULL ,
  `tag` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`work`, `tag`) ,
  INDEX `fk_work_has_tagWork_work` (`work` ASC) ,
  INDEX `fk_work_has_tagWork_tagWork` (`tag` ASC) ,
  CONSTRAINT `fk_work_has_tagWork_work`
    FOREIGN KEY (`work` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_tagWork_tagWork`
    FOREIGN KEY (`tag` )
    REFERENCES `knowledgetree`.`tagWork` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `knowledgetree`.`person_has_role`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`person_has_role` (
  `person` CHAR(20) NOT NULL ,
  `role` CHAR(20) NOT NULL ,
  PRIMARY KEY (`person`, `role`) ,
  INDEX `fk_person_has_role_person` (`person` ASC) ,
  INDEX `fk_person_has_role_role` (`role` ASC) ,
  CONSTRAINT `fk_person_has_role_person`
    FOREIGN KEY (`person` )
    REFERENCES `knowledgetree`.`person` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_person_has_role_role`
    FOREIGN KEY (`role` )
    REFERENCES `knowledgetree`.`role` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);

/*Data for the table `person_has_role` */

insert  into `person_has_role`(`person`,`role`) values ('ama','Auth');


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_work_relation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_work_relation` (
  `id` CHAR(20) NOT NULL ,
  `Name` VARCHAR(100) NULL DEFAULT NULL ,
  `Description` VARCHAR(1000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `knowledgetree`.`work_relatesto_work`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `knowledgetree`.`work_relatesto_work` (
  `work1` CHAR(20) NOT NULL ,
  `work2` CHAR(20) NOT NULL ,
  `relation_id` CHAR(20) NULL ,
  `sortorder` SMALLINT NULL ,
  PRIMARY KEY (`work1`, `work2`) ,
  INDEX `fk_work_has_work_work` (`work1` ASC) ,
  INDEX `fk_work_has_work_work1` (`work2` ASC) ,
  INDEX `fk_work_has_work_work_work_relation` (`relation_id` ASC) ,
  CONSTRAINT `fk_work_has_work_work`
    FOREIGN KEY (`work1` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_work_work1`
    FOREIGN KEY (`work2` )
    REFERENCES `knowledgetree`.`work` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_work_has_work_work_work_relation`
    FOREIGN KEY (`relation_id` )
    REFERENCES `knowledgetree`.`work_work_relation` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- View `knowledgetree`.`view_subject_subject`
-- -----------------------------------------------------

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_subject_subject` AS 
select
  `s1`.`id`           AS `sub1Id`,
  `s1`.`Name`         AS `subject1`,
  `s1`.`Description`  AS `subject1Description`,
  `s2`.`id`           AS `sub2Id`,
  `s2`.`Name`         AS `subject2`,
  `s2`.`Description`  AS `subject2Description`,
  `ssr`.`Name`        AS `relation`,
  `ssr`.`Description` AS `relation_description`
from (((`subject` `s1`
     join `subject` `s2`)
    join `subject_relatesto_subject` `srs`)
   join `subject_subject_relation` `ssr`)
where ((`s1`.`id` = `srs`.`Subject1`)
            and (`s2`.`id` = `srs`.`Subject2`)
            and (`srs`.`relation_id` = `ssr`.`id`));

-- -----------------------------------------------------
-- View `knowledgetree`.`view_subject_work`
-- -----------------------------------------------------
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_subject_work` AS 
select
  `s`.`Name`   AS `Subject`,
  `w`.`Title`  AS `Work`,
  `wsr`.`Name` AS `Relation`
from (((`subject` `s`
     join `work` `w`)
    join `subject_has_work` `sw`)
   join `work_subject_relation` `wsr`)
where ((`s`.`id` = `sw`.`Subject`)
            and (`w`.`id` = `sw`.`Work`)
            and (`sw`.`work_subject_relation` = `wsr`.`id`));


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
