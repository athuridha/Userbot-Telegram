from telethon import events
import random

# ID grup yang harus user gabung
REQUIRED_GROUP_ID = 2225134551

def load(client):
    @client.on(events.NewMessage(pattern=r'\.cekkhodam'))
    async def cekkhodam(event):
        # Ambil informasi pengguna
        user = await event.client.get_entity(event.sender_id)

        # Cek apakah user sudah bergabung dengan grup yang dimaksud
        try:
            # Ambil daftar peserta grup dengan ID REQUIRED_GROUP_ID
            participants = await event.client.get_participants(REQUIRED_GROUP_ID)

            # Cek apakah user ada dalam daftar peserta
            if any(participant.id == user.id for participant in participants):
                khodams = [
            "Khodam Gayung, cuy! Bisa bikin minuman lo jadi dingin kayak es batu yang baru keluar dari freezer. Soalnya, dia pernah ketemu sama es krim yang ngambek karena kelamaan di freezer.",
            "Khodam Kambing Ombong, bro! Kambing ini bisa nyuruh semua barang di sekitar lo biar beres sendiri. Katanya, dia dulu pernah jadi editor film horror, jadi ngerti cara bikin semua orang bingung.",
            "Khodam Ceker Ayam, sob! Setiap kali lo makan, ceker ini bikin makanan lo jadi kayak popcorn saat nonton film thriller. Makanya, dia dikasih gelar ‘Raja Crispy’ di kerajaan ayam.",
            "Khodam Kaki Seribu, men! Suka nyelinap ke sepatu lo, bikin kaki lo gatal-gatal. Karena, dia dulu nyoba jadi model sepatu untuk fashion show, tapi gagal karena terlalu banyak kaki.",
            "Khodam Jangkrik Pelawak, sissa! Suara jangkrik ini bikin lo ngakak terus-menerus. Dia pernah jadi pengisi acara stand-up comedy di festival serangga internasional.",
            "Khodam Kucing Berbicara, cuy! Kucing ini bisa ngomong dalam bahasa alien. Soalnya, dia belajar bahasa intergalaksi waktu jadi pengacara hewan peliharaan di luar angkasa.",
            "Khodam Topi Magician, nih! Semua topi di sekitar lo bisa terbang. Katanya, dia pernah dapet topi dari magician yang ngaku dapet ilmu sihirnya dari nenek moyangnya di dunia fantasi.",
            "Khodam Lampu Kuning, bebs! Lampu ini nyala hanya kalo lo nyari senter. Soalnya, dia dulu tinggal di dunia lampu yang semua orangnya lagi hobi main hide-and-seek.",
            "Khodam Terompet Tua, gais! Bikin lo susah tidur dengan bunyi terompet. Dia pernah ditinggal di pabrik terompet yang dibangun di atas sebuah gunung berapi.",
            "Khodam Sendok Perak, bro! Bikin semua makanan lo terasa kayak di restoran bintang lima. Katanya, dia dikasih hadiah sendok perak dari raja makanan.",
            "Khodam Tikus Bergigi, cuy! Ngigit barang-barang gak penting. Dia dulunya jadi superhero yang nyelamatin dunia dari tikus-tikus galaksi.",
            "Khodam Boneka Panggung, sob! Boneka-boneka lo joget sendiri. Soalnya, dia adalah sutradara boneka terkenal yang pernah bikin film boneka komedi.",
            "Khodam Kompor Berasap, sissa! Bikin masakan lo jadi pedes level dewa. Katanya, dia dulu jadi chef di restoran yang punya menu ‘super pedas’ yang diadopsi dari resep alien.",
            "Khodam Garpu Misterius, bebs! Sering ngilang pas lo makan. Soalnya, dia dulu tinggal di dapur yang penuh dengan garpu-garpu ninja.",
            "Khodam Bantal Ajaib, nih! Semua bantal jadi empuk kayak awan. Katanya, dia adalah bantal yang terpilih dari kontes bantal terempuk di negeri awan.",
            "Khodam Gelas Kopi, bro! Selalu ngisi gelas kopi lo dengan kopi panas. Dia dulu kerja di pabrik kopi yang terletak di puncak gunung berapi.",
            "Khodam Sabun Berkilau, cuy! Semua sabun jadi warna-warni. Katanya, dia dulu belajar dari pelukis pelangi yang juga guru sabun berkilau.",
            "Khodam Kunci Hilang, gaes! Semua kunci lo suka hilang. Soalnya, dia pernah dapet kunci dari dunia lain yang bikin semua kunci jadi mainan hilang.",
            "Khodam Penyapu Magis, bro! Bersihin lantai dengan sekali sapu. Katanya, dia dulu bikin penyapu dari pohon ajaib yang tumbuh di luar angkasa.",
            "Khodam Penghapus Tinta, sissa! Ngehapus tinta dengan sempurna. Soalnya, dia dulu ditugaskan sebagai penghapus tinta di laboratorium tinta dari masa depan.",
            "Khodam Kaleng Makanan, cuy! Makanan lo jadi lebih enak. Katanya, dia adalah kaleng yang pernah dipilih sebagai kaleng terbaik di kontes makanan ajaib.",
            "Khodam Stiker Hias, bebs! Semua stiker bersinar di gelap. Dia dulu tinggal di dunia stiker yang semua stiker bisa berbicara dan bercahaya.",
            "Khodam Tas Belanja, bro! Bisa nampung barang lebih banyak. Katanya, dia adalah tas belanja dari dimensi tanpa batas yang dibikin oleh para penyihir belanja.",
            "Khodam Bola Pingpong, gais! Bola pingpong lo jadi mantul banget. Soalnya, dia dulu jadi bola pingpong juara di turnamen pingpong intergalaksi.",
            "Khodam Buku Ajaib, cuy! Selalu kasih jawaban yang tepat. Dia adalah buku yang pernah ditulis oleh penulis dunia lain yang paham semua pertanyaan.",
            "Khodam Lampu Meja, nih! Cahaya dari lampu meja jadi lebih nyaman. Katanya, dia dulu tinggal di rumah lampu yang semua lampunya dibuat oleh para elf.",
            "Khodam Ranjang Susun, bebs! Semua ranjang jadi nyaman. Dia adalah ranjang dari dunia tidur yang semuanya dibangun di atas awan.",
            "Khodam Alat Musik, bro! Semua suara musik jadi simfoni. Katanya, dia dulunya alat musik yang dipilih untuk konser di planet luar angkasa.",
            "Khodam Papan Tulis, sissa! Ngehapus tulisan dengan sekali sapu. Dia adalah papan tulis dari sekolah ajaib yang semua tulisannya bisa dihapus dengan sihir.",
            "Khodam Obat Ajaib, cuy! Sembuhin penyakit kecil lo dengan cepat. Katanya, dia adalah obat yang didapat dari apotek rahasia di dunia ajaib.",
            "Khodam Botol Air, gais! Selalu ngasih air dingin. Dia adalah botol air yang dibikin oleh pembuat botol air dari pulau tropis.",
            "Khodam Hiasan Dinding, bebs! Hiasan dinding lo jadi lebih menarik. Katanya, dia pernah jadi hiasan dinding di galeri seni dari dimensi lain.",
            "Khodam Berita Pagi, bro! Selalu kasih berita baik tiap pagi. Dia adalah pengantar berita yang datang dari kota bahagia di luar angkasa.",
            "Khodam Pembuka Botol, sissa! Buka semua botol dengan mudah. Katanya, dia adalah alat pembuka botol dari pabrik pembuka botol galaksi.",
            "Khodam Panci Masak, cuy! Masakan lo jadi matang sempurna. Dia adalah panci yang pernah dipilih untuk memasak di restoran mewah di planet jauh.",
            "Khodam Gitar Bergetar, gais! Senar gitar lo terasa lebih ringan. Katanya, dia adalah gitar yang dipilih untuk konser rock di planet lain.",
            "Khodam Cangkir Kopi, bro! Setiap tegukan kopi lo jadi lebih nikmat. Dia adalah cangkir yang dikasih oleh barista dari kerajaan kopi ajaib.",
            "Khodam Sikat Gigi, sissa! Gigi lo terasa lebih bersih. Katanya, dia adalah sikat gigi yang dipilih oleh dokter gigi dari dunia fantastis.",
            "Khodam Tempat Tidur, cuy! Tidur lo jadi nyenyak banget. Dia adalah tempat tidur dari dunia tidur yang semua orangnya mimpi indah.",
            "Khodam Permen Karet, bro! Permen karet lo jadi lebih kenyal. Katanya, dia adalah permen karet yang dikasih oleh raja permen dari planet lain.",
            "Khodam Bingkai Foto, gais! Foto-foto lo jadi lebih indah. Dia adalah bingkai yang pernah dipilih untuk pameran foto di kota seni luar angkasa.",
            "Khodam Sarung Tangan, cuy! Tangan lo jadi hangat banget. Katanya, dia adalah sarung tangan dari dunia yang dinginnya melebihi es.",
            "Khodam Jam Dinding, nih! Selalu nunjukin waktu yang tepat. Dia adalah jam yang didapat dari toko jam di planet yang waktu berjalan lebih lambat.",
            "Khodam Tirai Jendela, bro! Ngatur cahaya masuk dengan pas. Katanya, dia adalah tirai yang dibuat oleh para ahli tirai dari dunia yang penuh warna.",
            "Khodam Kain Lap, sissa! Ngehapus noda dengan sekali usap. Dia adalah kain lap dari pabrik pembersih yang berada di dasar laut.",
            "Khodam Penghangat Ruangan, cuy! Ruangan lo jadi lebih hangat. Katanya, dia adalah penghangat yang dikasih oleh penjaga musim dingin dari utara.",
            "Khodam Meja Belajar, gais! Bikin belajar jadi lebih fokus. Dia adalah meja yang dulu dipilih untuk kelas paling pintar di dunia sekolah ajaib."
                ]
                
                # Pilih khodam secara acak
                khodam = random.choice(khodams)

                # Kirim respons sebagai balasan (reply) ke pesan yang memicu event
                await event.reply(f"🪄 **Hasil Cek Khodam:**\n\n{khodam}")
            else:
                # Jika user tidak ditemukan dalam grup
                await event.reply("yahh blum join gc dibiyohh makannya gak bisa 😛")
        
        except Exception as e:
            # Jika terjadi kesalahan, kirim pesan error
            await event.reply(f"Error: {str(e)}")

def add_commands(add_command):
    add_command('.cekkhodam', '🔮 Menampilkan khodam aneh dan lucu')
