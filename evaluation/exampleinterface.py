import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
indices = np.load("embedded/all/indices.npy")
titleabstracts = np.load("embedded/all/titleabstracts.npy")
fulltext = np.load("embedded/all/fulltext.npy")
fulltext_trunc = np.load("embedded/all/fulltext_trunc.npy")

def top_all_indices(patent_index, all_patent_indices, all_patent_embeddings):
    ind = np.where(all_patent_indices == patent_index)[0]
    patent_embedding = all_patent_embeddings[ind]
    
    # Normalize A and B for cosine similarity
    patent_embedding_norm = patent_embedding / np.linalg.norm(patent_embedding)
    all_patent_embeddings_norm = all_patent_embeddings / np.linalg.norm(all_patent_embeddings, axis=1, keepdims=True)

    # Compute cosine similarity
    similarities = np.dot(all_patent_embeddings_norm, patent_embedding_norm.T)

    # Combine C and D into a 2D array
    CD_combined = np.column_stack((similarities, all_patent_indices))

    # Sort by the first column (C) in descending order
    CD_sorted = CD_combined[np.argsort(CD_combined[:, 0])[::-1]]

    # Extract the sorted D values
    D_sorted = CD_sorted[:, 1]

    # D_sorted is the desired output
    return D_sorted

def find_title_abstract(ind):
    if os.path.exists(os.path.join("splitdata/titleabstracttexts", f"{ind}.txt")):
        with open(os.path.join("splitdata/titleabstracttexts", f"{ind}.txt"), "r") as f:
            titleabstract = f.read()
    elif os.path.exists(os.path.join("splitdata/titleabstracttexts1", f"{ind}.txt")):
        with open(os.path.join("splitdata/titleabstracttexts1", f"{ind}.txt"), "r") as f:
            titleabstract = f.read()
    elif os.path.exists(os.path.join("splitdata/titleabstracttexts2", f"{ind}.txt")):
        with open(os.path.join("splitdata/titleabstracttexts2", f"{ind}.txt"), "r") as f:
            titleabstract = f.read()
    elif os.path.exists(os.path.join("splitdata/titleabstracttexts3", f"{ind}.txt")):
        with open(os.path.join("splitdata/titleabstracttexts3", f"{ind}.txt"), "r") as f:
            titleabstract = f.read()
    else:
        titleabstract = "Not found"
    if len(titleabstract) <= 250:
        return titleabstract
    else:
        return titleabstract[:250] + "..."

def main():
    k = 5
    already_expanded = set()
    print("Enter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
    while True:
        user_input = input("> ").strip().lower()  # Get input, strip whitespace, and convert to lowercase
        
        if user_input == "index":
            print("Enter the patent application number:")
            user_input = str(input("> ").strip())
            titleabstract = find_title_abstract(user_input)
            if titleabstract == "Not found":
                print("Patent not found. Enter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
                continue
            else:
                print(f"Index {user_input}: {titleabstract}\n\n")
                already_expanded.add(user_input)
                print(f"Top {k} most similar:")
                count = 1
                top_all = top_all_indices(user_input, indices, fulltext)
                for ind in top_all:
                    if ind not in already_expanded:
                        print(f"Index {count}", find_title_abstract(ind),"\n")
                        count += 1
                        if count == k+1:
                            break
                print("\nSelect which patents to keep by entering the corresponding index numbers separated by commas, or 0 to select none:")
                user_input = input("> ").strip()
                if user_input == "0":
                    print("No new patents selected.")
                    print("\nEnter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
                    continue
                else:
                    selected_indices = user_input.split(",")
                    selected_indices = [int(ind) for ind in selected_indices]
                    selected_indices = [top_all[ind-1] for ind in selected_indices]
                    for ind in selected_indices:
                        already_expanded.add(ind)
                print("\nEnter a command ('index', 'expand', 'set k', 'save', or 'quit'")
        elif user_input == "expand":
            print("Currently expanded patents:", [str(ind) for ind in already_expanded])
            print("Enter the patent application number to expand:")
            user_input = input("> ").strip()
            titleabstract = find_title_abstract(user_input)
            if titleabstract == "Not found":
                print("Patent not found. Enter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
                continue
            else:
                already_expanded.add(ind)
                print(f"Top {k} most similar:")
                count = 1
                top_all = top_all_indices(user_input, indices, fulltext)
                for ind in top_all:
                    if ind not in already_expanded:
                        print(f"Index {count}", find_title_abstract(ind),"\n")
                        already_expanded.add(ind)
                        count += 1
                        if count == k+1:
                            break
                print("\nSelect which patents to keep by entering the corresponding index numbers separated by commas, or 0 to select none:")
                user_input = input("> ").strip()
                if user_input == "0":
                    print("No new patents selected.")
                    print("\nEnter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
                    continue
                else:
                    selected_indices = user_input.split(",")
                    selected_indices = [int(ind) for ind in selected_indices]
                    selected_indices = [top_all[ind-1] for ind in selected_indices]
                    for ind in selected_indices:
                        already_expanded.add(ind)
                print("\nEnter a command ('index', 'expand', 'set k', 'save', or 'quit'")
        elif user_input == "quit":
            print("Quitting program. Goodbye!")
            break
        elif user_input.startswith("set k"):
            print("Enter the value of k:")
            try:
                k = int(input("> ").strip())
                print(f"Set k to {k}.")
            except:
                print("Invalid input. Please enter an integer value for k next time.")
                print("\nEnter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
        elif user_input == "save":
            print("Enter a .txt filename to save the expanded patents to:")
            filename = input("> ").strip()
            with open(filename,"w") as f:
                for ind in already_expanded:
                    f.write(f"{ind}\n")
            print(f"Expanded patents saved to {filename}.")
            print("\nEnter a command ('index', 'expand', 'set k', 'save', or 'quit'):")
            
        else:
            print("\nInvalid command. Please enter 'index', 'expand', 'set k', 'save', or 'quit'.")

if __name__ == "__main__":
    main()