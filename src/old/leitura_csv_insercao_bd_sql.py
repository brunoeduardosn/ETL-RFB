
def leitura_csv_insercao_bd_sql(
    nome_arquivo, nome_tabela, sql_create_table, op_header, path_file
):
    """Função para leituras de csv da RFB para dataframe em loop e inserção no banco de dados postgres na tabela definida

    Args:
        nome_arquivo (String): Nome para pesquisa nos arquivos csv
        nome_tabela (String): Nome que será dado para tabela no banco de dados
        sql_create_table (String): SQL com criação da tabela com o mesmo esquema do csv
        op_header (String): Escolha de qual fonte é as informações (rfb ou ibge)
        path_file (String): Caminho de qual fonte é as informações (rfb ou ibge) será usada nas variáveis de anbiente
    """

    insert_start = time.time()

    try:
        pg_conn = psycopg2.connect(
            dbname=GetEnv("DB_NAME"),
            user=GetEnv("DB_USER"),
            password=GetEnv("DB_PASSWORD"),
            host=GetEnv("DB_HOST"),
            port=GetEnv("DB_PORT"),
        )
        cur = pg_conn.cursor()

        extracted_files = path_file

        # LER E INSERIR DADOS #

        Items = list(
            filter(
                lambda name: nome_arquivo in name, os.listdir(extracted_files)
            )
        )

        if len(Items) > 0:
            # Drop table antes do insert
            sql_1 = f"""DROP TABLE IF EXISTS "{nome_tabela}" CASCADE;"""
            cur.execute(sql_1)
            pg_conn.commit()

            # Criando tabela
            pg_conn.autocommit = True  #
            cur.execute(sql_create_table)
            pg_conn.commit()

            # Truncate the table in case you've already run the script before
            sql_2 = f"""TRUNCATE TABLE "{nome_tabela}";"""
            cur.execute(sql_2)
            pg_conn.commit()

            print_divisor_inicio_fim(
                f"Os arquivos contendo o nome {nome_arquivo} a seguir serão lidos e inseridos no banco de dados...",
                1,
            )
            for i, f in enumerate(Items, 1):
                print(f"{i} - Arquivo csv = {f}")

            for i, idx_arquivos_tmp in enumerate(
                tqdm(Items, bar_format="{l_bar}{bar}|", colour="green")
            ):  # o código \033[32m é usado para definir a cor do texto como verde e o código \033[0m é usado para redefinir a cor do texto para o padrão. Isso fará com que a barra de progresso seja exibida em verde.
                tmp_insert_start = time.time()

                print_divisor_inicio_fim(
                    f"Trabalhando no arquivo: {idx_arquivos_tmp} aguarde [...]",
                    0,
                )

                # GRAVAR DADOS NO BANCO

                path_file_csv = os.path.join(extracted_files, idx_arquivos_tmp)

                cur.execute("""SET CLIENT_ENCODING TO 'Utf-8';""")
                cur.execute("""SHOW client_encoding;""")

                if (op_header) == "rfb":
                    sql_3 = f"""
                    COPY {nome_tabela}
                    FROM '{path_file_csv}' --input full file path here.
                    DELIMITER ';' CSV;
                    """

                elif (op_header) == "ibge":
                    sql_3 = f"""
                    COPY {nome_tabela}
                    FROM '{path_file_csv}' --input full file path here.
                    DELIMITER ';' CSV HEADER;
                    """

                elif (op_header) == "anp":
                    sql_3 = f"""
                    COPY {nome_tabela}
                    FROM '{path_file_csv}' --input full file path here.
                    DELIMITER ';' CSV HEADER;
                    """

                elif (op_header) == "rais":
                    sql_3 = f"""
                    COPY {nome_tabela}
                    FROM '{path_file_csv}' --input full file path here.
                    DELIMITER ';' CSV;
                    """

                elif (op_header) == "ft":
                    sql_3 = f"""
                    COPY {nome_tabela}
                    FROM '{path_file_csv}' --input full file path here.
                    DELIMITER ';' CSV HEADER;
                    """

                elif (op_header) == "sgi":
                    sql_3 = f"""
                    COPY {nome_tabela}
                    FROM '{path_file_csv}' --input full file path here.
                    DELIMITER ';' CSV HEADER;
                    """

                else:
                    print_divisor_inicio_fim("!!! Opção não suportada !!!", 3)
                    log_retorno_erro("!!! Opção não suportada !!!")

                cur.execute(sql_3)
                pg_conn.commit()

                tmp_insert_end = time.time()

                print_parcial_final_log_inf_retorno(
                    "inserção no banco de dados",
                    tmp_insert_start,
                    tmp_insert_end,
                    idx_arquivos_tmp,
                    "parcial",
                )

            # close connection
            cur.close()

            # https://towardsdatascience.com/upload-your-pandas-dataframe-to-your-database-10x-faster-eb6dc6609ddf
            # https://www.enterprisedb.com/postgres-tutorials/how-import-and-export-data-using-csv-files-postgresql
            # https://stackoverflow.com/questions/4867272/invalid-byte-sequence-for-encoding-utf8

        else:
            print_divisor_inicio_fim(
                f"Sem arquivos na pasta ({extracted_files}) contendo o nome {nome_arquivo}",
                1,
            )

            log_retorno_info(
                f"Sem arquivos na pasta ({extracted_files}) contendo o nome {nome_arquivo}"
            )

            pass

        insert_end = time.time()

        print_parcial_final_log_inf_retorno(
            nome_arquivo, insert_start, insert_end, "", "final"
        )

    except Exception as text:
        log_retorno_erro(text)
