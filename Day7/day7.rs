const MAX_SIZE: u32 = 100000;
const TOTAL_SPACE: u32 = 70000000;
const FREE_NEEDED: u32 = 30000000; 

fn get_data() -> String {
    let input_args: Vec<String> = std::env::args().collect();
    let mut file_name: String = "input.txt".to_string();
    if input_args.len() > 1 {
        file_name = input_args[1].clone();
    }
    let mut data = std::fs::read_to_string(file_name).unwrap();
    if data.ends_with("\n") {
        data.pop();
    }
    return data;
}

struct Folder {
    pub name: String,
    pub size: Option<u32>,
    pub file_size_contents: u32,
    //pub files: Vec<String>,
    pub children: Vec<usize>,
    pub parent: Option<usize>,
}

impl Folder {
    pub fn add_file(&mut self, file_size: u32) {
        self.file_size_contents += file_size;
        if !self.size.is_none() {
            self.size = Some(self.size.unwrap() + file_size);
        }
        //self.files.push(file_name);
    }

    pub fn add_child(&mut self, child: usize) {
        self.children.push(child);
        self.size = None;
    }
}

pub struct FileSystem {
    folders: Vec<Folder>,
}

impl FileSystem {
    pub fn new_folder(&mut self, name: &str, parent: usize) -> usize {
        let next_index = self.folders.len();

        // We create the folder and add it to the struct
        self.folders.push(Folder {
            name: name.to_string(),
            size: Some(0),
            children: vec![],
            parent: Some(parent),
            //files: vec![],
            file_size_contents: 0,
        });

        next_index
    }

    pub fn number_folders(&self) -> usize {
        self.folders.len()
    }

    pub fn compute_size(&mut self, folder_index: usize) -> u32 {
        // We get the pre-existing value
        let stored_size = &self.folders[folder_index].size;
        if !stored_size.is_none() {
            return stored_size.unwrap().clone();
        }
        let mut size = self.folders[folder_index].file_size_contents.clone();

        // And now we transverse down and add
        for subfolder_index in self.folders[folder_index].children.clone() {
            size += self.compute_size(subfolder_index);
        }
        self.folders[folder_index].size = Some(size);
        size
    }

    pub fn return_all_sizes(&mut self) -> Vec<u32> {
        let number_folders = self.folders.len();
        let mut sizes = vec![];
        for index in 0..number_folders {
            sizes.push(self.compute_size(index))
        }
        sizes
    }
}

pub fn command_cd(folder_name: &str, current_folder: usize, file_system: &mut FileSystem) -> usize {
    match folder_name {
        ".." if !file_system.folders[current_folder].parent.is_none() => {
            return file_system.folders[current_folder].parent.unwrap().clone()
        }
        ".." if file_system.folders[current_folder].parent.is_none() => return current_folder,
        "/" => return current_folder,
        _ => (),
    };
    let new_index = file_system.new_folder(folder_name, current_folder.clone());
    file_system.folders[current_folder].add_child(new_index.clone());
    new_index
}

pub fn parse_command(line: &str, current_folder: usize, file_system: &mut FileSystem) -> usize {
    let split_line: Vec<&str> = line.split(" ").collect();
    if split_line[0] == "$" {
        if split_line[1] == "cd" {
            return command_cd(split_line[2], current_folder, file_system);
        }
        return current_folder;
    }
    if split_line[0] != "dir" {
        file_system.folders[current_folder].add_file(split_line[0].parse::<u32>().unwrap())
    }
    current_folder
}

fn main() {
    let data = get_data();
    let data_chunks: Vec<&str> = data.split("\n").collect();

    let mut file_system = FileSystem { folders: vec![] };

    // We add the root folder
    file_system.new_folder("/", 0);
    // We put itself as parrent so cd .. goes back to itself from ..
    // Note that this would not be safe if we had recursive functions
    // traversing up the tree, but it is not our case.
    let mut current_folder = 0 as usize; // We start from the root

    for chunk in data_chunks.iter() {
        current_folder = parse_command(chunk, current_folder, &mut file_system)
    }

    let folder_sizes = file_system.return_all_sizes();

    let result_part_1: u32 = folder_sizes
        .iter()
        .filter(|size| size < &&MAX_SIZE)
        .sum();

    // The total used space is the size of the root folder, which is at 0
    let need_to_free = FREE_NEEDED - (TOTAL_SPACE - folder_sizes[0]);
    let result_part_2 = folder_sizes
        .into_iter()
        .filter(|size| size > &need_to_free)
        .collect::<Vec<u32>>()
        .into_iter()
        .min()
        .unwrap();

    println!("The total size of the folders of less than {} is {}.", MAX_SIZE, result_part_1);
    println!("The size of the directory to delete is {}.", result_part_2)

}
