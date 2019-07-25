(ns demotivational-posters.core
  "Scrapes despair.com for demotivational poster titles and quotes"
  (:require
    [clojure.java.io :as io]
    [clojure.string :as string]
    [clj-http.client :as http]
    [hickory.core :as hc]
    [hickory.select :as hs])
  (:gen-class))

(def base-url "https://despair.com/collections/demotivators?page=")
(def pages [1 2])

(defn scrape-text []
  (reduce
    (fn [coll i]
      (let [hik (->> (http/get (str base-url i)) :body hc/parse hc/as-hickory)
            titles (map (comp first :content) (hs/select (hs/child (hs/class :info) (hs/class :title)) hik))
            bodies (map (comp first :content) (hs/select (hs/child (hs/class :info) (hs/class :price) (hs/tag :p)) hik))]
        (into coll (map vector titles bodies))))
    []
    pages))

(defn -main [out-file]
  (with-open [w (io/writer (or out-file "demotivational.txt"))]
    (doseq [[title body] (scrape-text)]
      (.write w (string/replace title "-" " "))
      (.newLine w)
      (.write w body)
      (.newLine w)
      (.newLine w))))
