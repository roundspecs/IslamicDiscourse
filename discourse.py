import sys
from json_handler import get_nodes, update_nodes
from constants import ROOT_NODE_ID


class Discourse:
    nodes = get_nodes()

    def start(self):
        self.__clear_screen()
        print("Assalamu alaikum")
        print(
            "Welcome to the discourse! Most of the arguments are taken from lectures"
            " and books of prominent scholars and daʿi's. This is a tool to help you "
            "understand the arguments and counter-arguments."
        )
        input("Press enter to continue")
        self.show_response(ROOT_NODE_ID)
        self.__clear_screen()
        print("Assalamu alaikum")

    def add_response(self, id: int):
        def __get_new_id():
            ids_taken = [0 for i in self.nodes]
            for id_taken in self.nodes.keys():
                ids_taken[id_taken] = 1
            new_id = len(self.nodes)
            for i in ids_taken:
                if i == 0:
                    new_id = i
                    break
            return new_id

        self.__clear_screen()
        print(
            f"Adding response to: {self.nodes[id]['person']}: {self.nodes[id]['message']} #{id}\n"
        )
        new_node = {
            "id": __get_new_id(),
            "person": (
                "Apologist" if self.nodes[id]["person"] == "Inquirer" else "Inquirer"
            ),
            "message": input("Enter message: "),
            "source": input("Enter source (or leave empty): "),
            "responses": [],
        }
        self.nodes[new_node["id"]] = new_node
        self.nodes[id]["responses"].append(new_node["id"])
        update_nodes(self.nodes)

    def edit_response(self, id: int):
        self.__clear_screen()
        print(f"{self.nodes[id]['person']}: {self.nodes[id]['message']} #{id}\n")
        print("1. Edit message")
        print("0. Back")
        ans = int(input("Enter number: "))
        if ans == 0:
            return
        elif ans == 1:
            self.nodes[id]["message"] = input("Enter message: ")
        update_nodes(self.nodes)
        self.edit_response(id)

    def remove_response(self, id: int):
        def __remove_response(id: int):
            children = self.nodes[id]["responses"]
            for child in children:
                self.__remove_response(child)
            del self.nodes[id]

        self.__clear_screen()
        if id == ROOT_NODE_ID:
            print("Cannot remove root node")
            input("Press enter to continue")
            self.show_response(id)
            return
        print(f"{self.nodes[id]['person']}: {self.nodes[id]['message']} #{id}")
        print("Are you sure you want to remove this response and all it's children?")
        ans = input("Enter [y/n]: ")
        if ans == "y":
            __remove_response(id)
        update_nodes(self.nodes)

    def show_response(self, id: int):
        self.__clear_screen()
        print(
            f"{self.nodes[id]['person']}: {self.nodes[id]['message']} #{self.nodes[id]['id']}"
        )
        if self.nodes[id]["source"]:
            print(f"Source: {self.nodes[id]['source']}")
        print()

        print("Responses:")
        for i, responce_id in enumerate(self.nodes[id]["responses"]):
            print(
                f"{i + 1}. {self.nodes[responce_id]['message']} #{self.nodes[responce_id]['id']}"
            )
        print("0. Back")

        ans = input(f"Enter number [or, add/edit/remove]: ")
        if ans == "add":
            self.add_response(id)
        elif ans == "edit":
            self.edit_response(id)
        elif ans == "remove":
            self.remove_response(id)
            return
        elif ans == "0":
            return
        else:
            self.show_response(self.nodes[id]["responses"][int(ans) - 1])
        self.show_response(id)

    def __clear_screen(self):
        sys.stdout.write("\033[H\033[J")
