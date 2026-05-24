import os
import random
import time
import polars as pl
from faker import Faker
import pyarrow as pa
import pyarrow.parquet as pq

def generate_giant_dataset(total_files=10, rows_per_file=100_000_000, batch_size=1_000_000):
    print(f"🚀 Pornire generare: {total_files} fișiere × {rows_per_file:,} rânduri = {total_files * rows_per_file:,} total cărți.")
    output_dir = "/mnt/gdrive/date_brute"
    os.makedirs(output_dir, exist_ok=True)
    
    fake = Faker()
    
    categorii_valide = ["Fiction", "Sci-Fi", "Mystery", "Biography", "History", "Fantasy", "Business", "Self-Help"]
    categorii_murdare = ["Ficttion", "SciFi", "mysteri", "BIOGRAPHY", "Unknown", "N/A"]
    
    print("⏳ Pre-generare nume de autori și cuvinte...")
    autori_baza = [fake.name() for _ in range(10_000)]
    cuvinte_baza = [fake.word().capitalize() for _ in range(5_000)]
    
    # REZOLVARE EROARE: Schimbăm pa.string() în pa.large_string() ca să se potrivească perfect cu Polars
    schema = pa.schema([
        ('book_id', pa.int64()),
        ('title', pa.large_string()),
        ('author', pa.large_string()),
        ('rating', pa.float64()),
        ('category', pa.large_string())
    ])
    
    global_id_counter = 1
    total_start_time = time.time()

    for file_idx in range(1, total_files + 1):
        file_path = os.path.join(output_dir, f"books_dataset_part_{file_idx}.parquet")
        file_start_time = time.time()
        print(f"\n📄 Se generează fișierul {file_idx}/{total_files} -> {file_path}")
        
        with pq.ParquetWriter(file_path, schema, compression='snappy') as writer:
            
            for batch_start in range(0, rows_per_file, batch_size):
                size = min(batch_size, rows_per_file - batch_start)
                
                # Generare rapidă liste
                ids = list(range(global_id_counter, global_id_counter + size))
                global_id_counter += size
                
                w1 = random.choices(cuvinte_baza, k=size)
                w2 = random.choices(cuvinte_baza, k=size)
                w3 = random.choices(cuvinte_baza, k=size)
                titles = [f"{a} {b} {c}" for a, b, c in zip(w1, w2, w3)]
                
                authors = random.choices(autori_baza, k=size)
                categories = random.choices(categorii_valide, k=size)
                ratings = [round(random.uniform(1.0, 5.0), 2) for _ in range(size)]
                
                # "Murdărire" date optimizată
                for i in range(size):
                    r = random.random()
                    if r < 0.03:
                        titles[i] = None
                    elif r < 0.05:
                        authors[i] = None
                    elif r < 0.07:
                        ratings[i] = None
                    elif r < 0.08:
                        ratings[i] = round(random.uniform(6.0, 10.0), 2)
                    elif r < 0.09:
                        categories[i] = random.choice(categorii_murdare)
                    elif r < 0.10:
                        categories[i] = None
                
                # Creare DataFrame Polars cu tipuri explicite
                df = pl.DataFrame({
                    "book_id": ids,
                    "title": titles,
                    "author": authors,
                    "rating": ratings,
                    "category": categories
                }, schema={
                    "book_id": pl.Int64, 
                    "title": pl.String, 
                    "author": pl.String, 
                    "rating": pl.Float64, 
                    "category": pl.String
                })
                
                # Conversia va respecta acum schema exactă datorită lui large_string
                arrow_table = df.to_arrow()
                writer.write_table(arrow_table)
                
                print(f"   💾 Adăugat batch de {size:,} rânduri în fișier. ID curent: {global_id_counter-1:,}")
                
        print(f"✨ Fișierul {file_idx} a fost finalizat în {time.time() - file_start_time:.2f}s")
        
    print(f"\n🎉 Succes total! Toate cele {total_files} fișiere au fost scrise în {time.time() - total_start_time:.2f}s")

generate_giant_dataset(total_files=5, rows_per_file=100_000_000, batch_size=1_000_000)